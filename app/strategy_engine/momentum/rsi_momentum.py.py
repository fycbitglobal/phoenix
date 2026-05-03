# app/strategy_engine/momentum/rsi_momentum.py
import pandas as pd
import pandas_ta as ta
from app.strategy_engine.base_strategy import BaseStrategy
from app.core.types import Signal, OrderSide
from typing import Optional

class RSIMomentumStrategy(BaseStrategy):
    def __init__(self, symbols: list, period: int = 14):
        super().__init__("Momentum_RSI", symbols)
        self.period = period
        self.history = {symbol: [] for symbol in symbols}

    async def on_candle(self, candle: dict) -> Optional[Signal]:
        symbol = candle['symbol']
        self.history[symbol].append(candle)
        if len(self.history[symbol]) < self.period: return None

        df = pd.DataFrame(self.history[symbol])
        rsi = ta.rsi(df['close'], length=self.period)
        current_rsi = rsi.iloc[-1]

        if current_rsi > 60: 
            return Signal(symbol=symbol, side=OrderSide.BUY, strength=0.6, strategy_name=self.name)
        elif current_rsi < 40: 
            return Signal(symbol=symbol, side=OrderSide.SELL, strength=0.6, strategy_name=self.name)
        
        return None
