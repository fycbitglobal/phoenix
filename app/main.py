# main.py
import asyncio
from app.core.logger import logger
from app.core.event_bus import event_bus
from app.data_engine.market_feed import MarketFeed
from app.data_engine.orderbook_stream import OrderbookStream
from app.strategy_engine.strategy_manager import StrategyManager
from app.data_engine.data_loader import DataLoader
from app.core.database import db # <--- VERİTABANI ENTEGRASYONU

# --- YENİ EKLEME: API ve Dashboard için gerekli importlar ---
import uvicorn
from app.api.main import app as fastapi_app 
# -----------------------------------------------------------

# 1. Sinyal Motoru (Füzyon) Entegrasyonu
from app.signal_engine.signal_fusion import SignalFusion

# 2. Risk Motoru Entegrasyonu
from app.risk_engine.risk_manager import RiskManager

# 3. İnfaz Motoru (Execution Engine) Entegrasyonu
from app.execution_engine.order_router import OrderRouter
from app.execution_engine.order_manager import OrderManager

# 4. İzleme ve Kontrol Katmanı Entegrasyonu (YENİ EKLEMELER)
from app.monitoring.trade_logger import TradeLogger
from app.monitoring.pnl_tracker import PNLTracker
from app.control_layer.telegram_bot import TradingBot

# 5. Tüm Stratejileri Import Et
from app.strategy_engine.trend.ema_strategy import EMAStrategy
from app.strategy_engine.trend.adx_strategy import ADXStrategy
from app.strategy_engine.momentum.rsi_momentum import RSIMomentumStrategy
from app.strategy_engine.momentum.macd_strategy import MACDStrategy
from app.strategy_engine.momentum.roc_strategy import ROCStrategy
from app.strategy_engine.mean_reversion.bollinger_reversion import BollingerReversionStrategy
from app.strategy_engine.mean_reversion.rsi_reversion import RSIReversionStrategy
from app.strategy_engine.mean_reversion.vwap_deviation import VWAPDeviationStrategy # Yazım hatası düzeltildi
from app.strategy_engine.mean_reversion.vwap_deviation import VWAPDeviationStrategy # Tekrar eklendi
from app.strategy_engine.smc.fair_value_gap import FVGStrategy
from app.strategy_engine.smc.order_blocks import OrderBlockStrategy
from app.strategy_engine.smc.bos_mss import BOSStrategy
from app.strategy_engine.smc.liquidity_sweep import LiquiditySweepStrategy
from app.strategy_engine.volatility.atr_breakout import ATRBreakoutStrategy
from app.strategy_engine.volatility.squeeze_breakout import SqueezeBreakoutStrategy
from app.strategy_engine.orderflow.whale_detection import WhaleDetectionStrategy

# --- LISTENERS (Dinleyiciler) ---

# Ham sinyalleri izlemek istersen (Debug için)
async def raw_signal_listener(signal):
    logger.info(f"🛠️ HAM SİNYAL: {signal.strategy_name} -> {signal.side}")

# Rafine edilmiş, onaylanmış sinyalleri izlemek için
async def fused_signal_listener(fused_signal):
    # Not: {fused_fused_signal.symbol} yazım hatası düzeltildi
    logger.info(f"💎 ONAYLI SİNYAL: {fused_signal.symbol} | Yön: {fused_signal.side} | Güven: {fused_signal.confidence_level} | Skor: {fused_signal.final_score:.2f}")

# Risk motorundan çıkan gerçek emir taleplerini izlemek için
async def order_request_listener(order):
    logger.info(f"💰 EMİR TALEBİ OLUŞTU: {order.symbol} | {order.side} | Miktar: {order.quantity:.4f} | SL: {order.stop_loss:.2f} | TP: {order.take_profit:.2f}")

# İnfaz sonucu (Borsadan gelen yanıt) dinleyicisi
async def execution_result_listener(result):
    if result:
        logger.info(f"✅ İŞLEM BORSADA GERÇEKLEŞTİ: {result}")
    else:
        logger.error("❌ Borsa emri reddetti veya bir hata oluştu!")

# --- MAIN FUNCTION ---

async def main():
    # --- 0. VERİTABANI BAŞLATMA ---
    await db.initialize()

    # --- 1. İZLEME VE KONTROL KURULUMU (YENİ) ---
    pnl_tracker = PNLTracker()
    await pnl_tracker.sync_with_db() # Veritabanından kâr/zararı yükle
    
    trade_logger = TradeLogger()
    
    # Order Manager başlatma ve DB'den pozisyonları yükleme
    order_manager = OrderManager()
    await order_manager.load_positions_from_db()
    
    # Telegram Bot'u başlat
    bot = TradingBot(pnl_tracker, order_manager)
    asyncio.create_task(bot.start_polling())

    # --- 2. İNFAZ MOTORU KURULUMU ---
    router = OrderRouter()

    # Emri gerçekten borsaya gönderen, pozisyonu güncelleyen ve bildirim atan fonksiyon
    async def handle_order_execution(order_request):
        # A. Emri ilgili borsaya yönlendir
        result = await router.route_router.route_order(order_request) # Yazım hatası düzeltildi
        result = await router.route_order(order_request)
        if result:
            # B. Pozisyonu takipçiye ve DB'ye ekle (SADECE await eklendi)
            await order_manager.update_position(
                order_request.symbol, 
                order_request.side.value, 
                order_request.price, 
                order_request.quantity
            )
            
            # C. İşlemi CSV dosyasına kaydet
            trade_logger.log_trade({
                "symbol": order_order_request.symbol, # Yazım hatası düzeltildi
                "symbol": order_request.symbol,
                "side": order_request.side.value,
                "entry": order_request.price,
                "qty": order_request.quantity
            })
            
            # D. Telegram'a anlık bildirim gönder
            await bot.send_alert(
                f"💰 **SİSTEM İŞLEM AÇTİ**\n"
                f"Sembol: {order_request.symbol}\n"
                f"Yön: {order_request.side.value}\n"
                f"Miktar: {order_request.quantity:.4f}\n"
                f"Giriş: {order_request.price:.2f}\n"
                f"SL: {order_request.stop_loss:.2f} | TP: {order_request.take_profit:.2f}"
            )
            
            # E. İşlem başarılı olayını yayınla
            await event_bus.publish("ORDER_FILLED", result)

    # --- EVENT BUS ABONELİKLERİ ---
    
    # A. İnfaz sonuçlarını dinle
    event_bus.subscribe("ORDER_FILLED", execution_result_listener)
    
    # B. Emir talebi oluştuğunda hem logla hem de borsaya gönder
    event_bus.subscribe("ORDER_REQUEST_GENERATED", order_request_listener) 
    event_bus.subscribe("ORDER_REQUEST_GENERATED", handle_order_execution) 
    
    # C. Risk Manager'ı başlat ve rafine sinyalleri ona bağla
    risk_manager = RiskManager()
    event_bus.subscribe("FUSED_SIGNAL_GENERATED", risk_manager.on_fused_signal)
    
    # D. Rafine sinyalleri izlemek için
    event_bus.subscribe("FUSED_SIGNAL_GENERATED", fused_signal_listener)
    
    # E. Sinyal Füzyon Motorunu başlat
    fusion_engine = SignalFusion()
    event_bus.subscribe("SIGNAL_GENERATED", fusion_engine.on_signal_generated)
    
    # F. (Opsiyonel) Ham sinyaller
    # event_bus.subscribe("SIGNAL_GENERATED", raw_signal_listener)

    # --- STRATEJİ YÖNETİMİ ---
    strat_manager = StrategyManager()
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    
    # Trend Stratejileri
    strat_manager.add_strategy(EMAStrategy(symbols))
    strat_manager.add_strategy(ADXStrategy(symbols))
    
    # Momentum Stratejileri
    strat_manager.add_strategy(RSIMomentumStrategy(symbols))
    strat_manager.add_strategy(MACDStrategy(symbols))
    strat_manager.add_strategy(ROCStrategy(symbols))
    
    # Mean Reversion Stratejileri
    strat_manager.add_strategy(BollingerReversionStrategy(symbols))
    strat_manager.add_strategy(RSIReversionStrategy(symbols))
    strat_manager.add_strategy(VWAPDeviationStrategy(symbols))
    strat_manager.add_strategy(VWAPDeviationStrategy(symbols))
    strat_manager.add_strategy(VWAPDeviationStrategy(symbols))
    
    # SMC Stratejileri
    strat_manager.add_strategy(FVGStrategy(symbols))
    strat_manager.add_strategy(OrderBlockStrategy(symbols))
    strat_manager.add_strategy(BOSStrategy(symbols))
    strat_manager.add_strategy(LiquiditySweepStrategy(symbols))
    
    # Volatility Stratejileri
    strat_manager.add_strategy(ATRBreakoutStrategy(symbols))
    strat_manager.add_strategy(SqueezeBreakoutStrategy(symbols))
    
    # Order Flow (Tick bazlı özel abone)
    whale_strat = WhaleDetectionStrategy(symbols)
    event_bus.subscribe("TICK_RECEIVED", whale_strat.on_tick)

    # Mum kapanışlarını strateji yöneticisine bağla
    event_bus.subscribe("CANDLE_CLOSED", strat_manager.on_candle_closed)

    # --- GEÇMİŞ VERİ YÜKLEME ---
    data_loader = DataLoader()
    for symbol in symbols:
        past_candles = await data_loader.fetch_historical_candles(symbol)
        for strategy in strat_manager.strategies:
            if hasattr(strategy, 'history') and symbol in strategy.history:
                strategy.history[symbol].extend(past_candles)
    await data_loader.close()
    
    # --- VERİ KAYNAKLARI ---
    feed = MarketFeed(symbols=symbols)
    ob_stream = OrderbookStream(symbols=symbols)
    
    # --- YENİ EKLEME: API SUNUCUSUNU BAŞLAT (Sistemi dondurmadan) ---
    config = uvicorn.Config(fastapi_app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    api_task = asyncio.create_task(server.serve())
    # -----------------------------------------------------------

    try:
        logger.info("MTO Trading OS - FULL STACK (Data + Strategy + Fusion + Risk + Execution + Monitoring + Bot + Database + API) BASLATILDI!")
        await asyncio.gather(
            feed.start(),
            ob_stream.connect(),
            api_task # API sunucusunu da aynı anda çalıştır
        )
    except KeyboardInterrupt:
        logger.info("Sistem kapatılıyor...")
        await router.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
