# app/strategy_engine/volatility/squeeze_breakout.py
import pandas as pd
import pandas_ta as ta
from app.strategy_engine.base_strategy import BaseStrategy
from app.core.types import Signal, OrderSide
from typing import Optional

class SqueezeBreakoutStrategy(BaseStrategy):
    def __init__(self, symbols: list):
        super().__init__("Volatility_Squeeze", symbols)
        self.history = {symbol: [] for symbol in symbols}

    async def on_candle(self, candle: dict) -> Optional[Signal]:
        symbol = candle['symbol']
        self.history[symbol].append(candle)
        if len(self.history[symbol]) < 20: return None
        
        df = pd.DataFrame(self.history[symbol])
        bb = ta.bbands(df['close'], length=20)
        # BB genişliği düşükse "squeeze" vardır
        bandwidth = (bb['BBU_20_2.0'].iloc[-1] - bb['BBL_20_2.0'].iloc[-1]) / bb['BBM_20_2.0'].iloc[-1]
        
        if bandwidth < 0.01: # Çok dar bant
            if candle['close'] > bb['BBU_20_2.0'].iloc[-1]:
                return Signal(symbol=symbol, side=OrderSide.BUY, strength=0.8, strategy_name=self.name)
            if candle['close'] < bb['BBL_20_2.0'].iloc[-1]:
                return Signal(symbol=symbol, side=OrderSide.SELL, strength=0.8, strategy_name=self.name)
        return None
