# app/risk_engine/risk_manager.py
from app.core.event_bus import event_bus
from app.core.logger import logger
from app.core.types import OrderRequest, OrderType
from app.signal_engine.signal_model import FusedSignal
from .position_sizer import PositionSizer
from .stop_loss_engine import StopLossEngine
from .portfolio_risk import PortfolioRisk
from .drawdown_protection import DrawdownProtection

class RiskManager:
    def __init__(self):
        self.sizer = PositionSizer()
        self.sl_engine = StopLossEngine()
        self.portfolio = PortfolioRisk()
        self.protection = DrawdownProtection()
        
        # Simülasyon için başlangıç bakiyesi (Gerçekte API'den çekilir)
        self.current_balance = 10000.0 

    async def on_fused_signal(self, fused_signal: FusedSignal):
        """Füzyon motorundan gelen kaliteli sinyalleri risk filtresinden geçirir."""
        logger.info(f"🛡️ Risk Kontrolü Başladı: {fused_signal.symbol}")

        # 1. Drawdown Kontrolü (Sistem genelinde stop var mı?)
        if not self.protection.check_drawdown(self.current_balance):
            return

        # 2. Portföy Kontrolü (Çok fazla açık işlem var mı?)
        if not self.portfolio.can_open_new_position():
            logger.warning(f"⚠️ İşlem reddedildi: Maksimum açık pozisyon limitine ulaşıldı.")
            return

        # 3. Fiyat ve Risk Hesaplamaları
        # (Normalde giriş fiyatı anlık tick verisinden alınır, şimdilik varsayılan kullanıyoruz)
        entry_price = 60000.0 # Örnek fiyat (BTC)
        sl, tp = self.sl_engine.calculate_sl_tp(fused_signal.side, entry_price)
        
        # 4. Pozisyon Büyüklüğü Hesaplama
        quantity = self.sizer.calculate_size(self.current_balance, entry_price, sl)

        if quantity <= 0:
            logger.error("❌ Pozisyon büyüklüğü hesaplanamadı. İşlem reddedildi.")
            return

        # 5. EMİR TALEBİ OLUŞTUR (OrderRequest)
        order_request = OrderRequest(
            symbol=fused_signal.symbol,
            side=fused_signal.side,
            order_type=OrderType.MARKET,
            quantity=quantity,
            price=entry_price,
            stop_loss=sl,
            take_profit=tp
        )

        logger.info(f"✅ RİSK ONAYLANDI: {fused_signal.symbol} | Miktar: {quantity:.4f} | SL: {sl:.2f} | TP: {tp:.2f}")
        
        # İNFAZ MOTORUNA (Execution Engine) GÖNDER
        await event_bus.publish("ORDER_REQUEST_GENERATED", order_request)
