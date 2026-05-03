# app/strategy_engine/momentum/macd_strategy.py
import pandas as pd
import pandas_ta as ta
from app.strategy_engine.base_strategy import BaseStrategy
from app.core.types import Signal, OrderSide
from typing import Optional

class MACDStrategy(BaseStrategy):
    def __init__(self, symbols: list):
        super().__init__("Momentum_MACD", symbols)
        self.history = {symbol: [] for symbol in symbols}

    async def on_candle(self, candle: dict) -> Optional[Signal]:
        symbol = candle['symbol']
        self.history[symbol].append(candle)
        if len(self.history[symbol]) < 30: return None
        try:
            df = pd.DataFrame(self.history[symbol])
            macd = ta.macd(df['close']) 
            macd_line = macd['MACD_12_26_9'].iloc[-1]
            signal_line = macd['MACDs_12_26_9'].iloc[-1]
            if macd_line > signal_line:
                return Signal(symbol=symbol, side=OrderSide.BUY, strength=0.7, strategy_name=self.name)
            elif macd_line < signal_line:
                return Signal(symbol=symbol, side=OrderSide.SELL, strength=0.7, strategy_name=self.name)
        except Exception:
            pass
        return None
