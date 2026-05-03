# app/strategy_engine/momentum/roc_strategy.py
import pandas as pd
import pandas_ta as ta
from app.strategy_engine.base_strategy import BaseStrategy
from app.core.types import Signal, OrderSide
from typing import Optional

class ROCStrategy(BaseStrategy):
    def __init__(self, symbols: list):
        super().__init__("Momentum_ROC", symbols)
        self.history = {symbol: [] for symbol in symbols}

    async def on_candle(self, candle: dict) -> Optional[Signal]:
        symbol = candle['symbol']
        self.history[symbol].append(candle)
        if len(self.history[symbol]) < 14: return None
        
        df = pd.DataFrame(self.history[symbol])
        roc = ta.roc(df['close'], length=14).iloc[-1]
        
        if roc > 1.0: return Signal(symbol=symbol, side=OrderSide.BUY, strength=0.6, strategy_name=self.name)
        if roc < -1.0: return Signal(symbol=symbol, side=OrderSide.SELL, strength=0.6, strategy_name=self.name)
        return None
