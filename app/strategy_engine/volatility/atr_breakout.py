# app/strategy_engine/volatility/atr_breakout.py
import pandas as pd
import pandas_ta as ta
from app.strategy_engine.base_strategy import BaseStrategy
from app.core.types import Signal, OrderSide
from typing import Optional

class ATRBreakoutStrategy(BaseStrategy):
    def __init__(self, symbols: list):
        super().__init__("Volatility_ATR", symbols)
        self.history = {symbol: [] for symbol in symbols}

    async def on_candle(self, candle: dict) -> Optional[Signal]:
        symbol = candle['symbol']
        self.history[symbol].append(candle)
        if len(self.history[symbol]) < 14: return None

        df = pd.DataFrame(self.history[symbol])
        atr = ta.atr(df['high'], df['low'], df['close'], length=14).iloc[-1]
        
        # Basit Breakout: Fiyat, önceki mumun yükseğinin ATR kadar üzerine çıkarsa
        prev_high = df['high'].iloc[-2]
        current_close = df['close'].iloc[-1]

        if current_close > (prev_high + atr):
            return Signal(symbol=symbol, side=OrderSide.BUY, strength=0.8, strategy_name=self.name)
        elif current_close < (df['low'].iloc[-2] - atr):
            return Signal(symbol=symbol, side=OrderSide.SELL, strength=0.8, strategy_name=self.name)

        return None
