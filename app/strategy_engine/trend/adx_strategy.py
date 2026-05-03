# app/strategy_engine/trend/adx_strategy.py
import pandas as pd
import pandas_ta as ta
from app.strategy_engine.base_strategy import BaseStrategy
from app.core.types import Signal, OrderSide
from typing import Optional

class ADXStrategy(BaseStrategy):
    def __init__(self, symbols: list):
        super().__init__("Trend_ADX", symbols)
        self.history = {symbol: [] for symbol in symbols}

    async def on_candle(self, candle: dict) -> Optional[Signal]:
        symbol = candle['symbol']
        self.history[symbol].append(candle)
        if len(self.history[symbol]) < 20: return None
        
        df = pd.DataFrame(self.history[symbol])
        adx = ta.adx(df['high'], df['low'], df['close'])
        current_adx = adx['ADX_14'].iloc[-1]
        
        # ADX > 25 ise trend güçlüdür. Yönü belirlemek için close > ema20 kullanılır.
        if current_adx > 25:
            # Basit yön tayini
            side = OrderSide.BUY if candle['close'] > df['close'].iloc[-20:].mean() else OrderSide.SELL
            return Signal(symbol=symbol, side=side, strength=0.7, strategy_name=self.name)
        return None
