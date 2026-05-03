# app/strategy_engine/mean_reversion/rsi_reversion.py
import pandas as pd
import pandas_ta as ta
from app.strategy_engine.base_strategy import BaseStrategy
from app.core.types import Signal, OrderSide
from typing import Optional

class RSIReversionStrategy(BaseStrategy):
    def __init__(self, symbols: list):
        super().__init__("MeanRev_RSI", symbols)
        self.history = {symbol: [] for symbol in symbols}

    async def on_candle(self, candle: dict) -> Optional[Signal]:
        symbol = candle['symbol']
        self.history[symbol].append(candle)
        if len(self.history[symbol]) < 14: return None
        
        df = pd.DataFrame(self.history[symbol])
        rsi = ta.rsi(df['close'], length=14).iloc[-1]
        
        if rsi < 30: return Signal(symbol=symbol, side=OrderSide.BUY, strength=0.7, strategy_name=self.name)
        if rsi > 70: return Signal(symbol=symbol, side=OrderSide.SELL, strength=0.7, strategy_name=self.name)
        return None
