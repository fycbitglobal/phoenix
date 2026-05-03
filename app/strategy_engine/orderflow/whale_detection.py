# app/strategy_engine/orderflow/whale_detection.py
from app.core.event_bus import event_bus
from app.core.types import Signal, OrderSide
from app.strategy_engine.base_strategy import BaseStrategy

class WhaleDetectionStrategy(BaseStrategy):
    def __init__(self, symbols: list):
        super().__init__("OrderFlow_Whale", symbols)

    async def on_tick(self, tick): # Mum değil, Tick ile çalışır
        # Eğer tek bir işlem, ortalamanın 10 katı hacme sahipse balina işlemi say
        if tick.volume > 10.0: # Örn: 10 BTC'lik tek işlem
            side = OrderSide.BUY if tick.price > 0 else OrderSide.SELL # Basit mantık
            await event_bus.publish("SIGNAL_GENERATED", Signal(
                symbol=tick.symbol, side=side, strength=0.5, strategy_name=self.name
            ))

    async def on_candle(self, candle): return None
