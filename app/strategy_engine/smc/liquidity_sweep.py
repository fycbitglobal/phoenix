# app/strategy_engine/smc/liquidity_sweep.py
import pandas as pd
from app.strategy_engine.base_strategy import BaseStrategy
from app.core.types import Signal, OrderSide
from typing import Optional

class LiquiditySweepStrategy(BaseStrategy):
    def __init__(self, symbols: list):
        super().__init__("SMC_LiqSweep", symbols)
        self.history = {symbol: [] for symbol in symbols}

    async def on_candle(self, candle: dict) -> Optional[Signal]:
        symbol = candle['symbol']
        self.history[symbol].append(candle)
        if len(self.history[symbol]) < 20: return None
        
        df = pd.DataFrame(self.history[symbol])
        prev_low = df['low'].iloc[-20:-1].min()
        
        # Fiyat eski dibin altına indi ama mum yukarıda kapattı (Süpürme)
        if candle['low'] < prev_low and candle['close'] > prev_low:
            return Signal(symbol=symbol, side=OrderSide.BUY, strength=0.8, strategy_name=self.name)
        
        prev_high = df['high'].iloc[-20:-1].max()
        if candle['high'] > prev_high and candle['close'] < prev_high:
            return Signal(symbol=symbol, side=OrderSide.SELL, strength=0.8, strategy_name=self.name)
            
        return None
