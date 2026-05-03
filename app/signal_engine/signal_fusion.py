# app/signal_engine/signal_fusion.py
import asyncio
from datetime import datetime
from app.core.event_bus import event_bus
from app.core.logger import logger
from app.core.types import Signal, OrderSide
from app.signal_engine.signal_model import FusedSignal
from app.signal_engine.scoring_engine import ScoringEngine
from app.signal_engine.signal_filter import SignalFilter

class SignalFusion:
    def __init__(self):
        self.scoring_engine = ScoringEngine()
        self.filter = SignalFilter(min_score=0.4)
        # Sinyalleri geçici olarak tutmak için bir tampon (buffer)
        # { 'BTCUSDT': {'BUY': [Signal1, Signal2], 'SELL': []} }
        self.buffer = {}

    async def on_signal_generated(self, signal: Signal):
        """Sinyalleri yakalar ve tampona ekler."""
        symbol = signal.symbol
        side = signal.side.value # "BUY" veya "SELL"

        if symbol not in self.buffer:
            self.buffer[symbol] = {"BUY": [], "SELL": []}
        
        self.buffer[symbol][side].append(signal)
        
        # Sinyal geldiğinde hemen birleştirme işlemini tetikle
        await self.fuse_signals(symbol, side)

    async def fuse_signals(self, symbol: str, side: str):
        signals = self.buffer[symbol][side]
        if not signals: return

        # Sadece aynı yöndeki sinyalleri topla
        final_score = self.scoring_engine.calculate_score(signals)
        
        # Güven seviyesini belirle
        confidence = "LOW"
        if final_score > 0.7: confidence = "HIGH"
        elif final_score > 0.4: confidence = "MEDIUM"

        fused = FusedSignal(
            symbol=symbol,
            side=OrderSide.BUY if side == "BUY" else OrderSide.SELL,
            final_score=final_score,
            contributing_strategies=[s.strategy_name for s in signals],
            confidence_level=confidence
        )

        # Filtreden geçir
        if self.filter.is_valid(fused):
            logger.info(f"💎 KALİTELİ SİNYAL ONAYLANDI: {symbol} {side} | Skor: {final_score:.2f} | Güven: {confidence}")
            # RİSK MOTORUNA GÖNDER
            await event_bus.publish("FUSED_SIGNAL_GENERATED", fused)
        
        # İşlem bittikten sonra tamponu temizle (yeni sinyalleri beklemek için)
        self.buffer[symbol][side] = []
