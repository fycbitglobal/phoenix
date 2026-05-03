# app/strategy_engine/mean_reversion/vwap_deviation.py
import pandas as pd
import pandas_ta as ta
from app.strategy_engine.base_strategy import BaseStrategy
from app.core.types import Signal, OrderSide
from typing import Optional

class VWAPDeviationStrategy(BaseStrategy):
    def __init__(self, symbols: list):
        super().__init__("MeanRev_VWAP", symbols)
        self.history = {symbol: [] for symbol in symbols}

    async def on_candle(self, candle: dict) -> Optional[Signal]:
        symbol = candle['symbol']
        self.history[symbol].append(candle)
        if len(self.history[symbol]) < 20: return None
        
        df = pd.DataFrame(self.history[symbol])
        vwap = ta.vwap(df['high'], df['low'], df['close'], df['volume'])
        current_vwap = vwap.iloc[-1]
        current_close = candle['close']
        
        deviation = (current_close - current_vwap) / current_vwap
        
        if deviation < -0.01: return Signal(symbol=symbol, side=OrderSide.BUY, strength=0.6, strategy_name=self.name)
        if deviation > 0.01: return Signal(symbol=symbol, side=OrderSide.SELL, strength=0.6, strategy_name=self.name)
        return None
