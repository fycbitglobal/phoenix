# app/strategy_engine/mean_reversion/bollinger_reversion.py
import pandas as pd
import pandas_ta as ta
from app.strategy_engine.base_strategy import BaseStrategy
from app.core.types import Signal, OrderSide
from typing import Optional

class BollingerReversionStrategy(BaseStrategy):
    def __init__(self, symbols: list):
        super().__init__("MeanRev_Bollinger", symbols)
        self.history = {symbol: [] for symbol in symbols}

    async def on_candle(self, candle: dict) -> Optional[Signal]:
        symbol = candle['symbol']
        self.history[symbol].append(candle)
        if len(self.history[symbol]) < 20: return None

        df = pd.DataFrame(self.history[symbol])
        bbands = ta.bbands(df['close'], length=20, std=2)
        
        lower_band = bbands['BBL_20_2.0'].iloc[-1]
        upper_band = bbands['BBU_20_2.0'].iloc[-1]
        current_close = df['close'].iloc[-1]

        # Fiyat alt banda değdiyse veya altındaysa -> Yukarı döner (BUY)
        if current_close <= lower_band:
            return Signal(symbol=symbol, side=OrderSide.BUY, strength=0.7, strategy_name=self.name)
        # Fiyat üst banda değdiyse veya üstündeyse -> Aşağı döner (SELL)
        elif current_close >= upper_band:
            return Signal(symbol=symbol, side=OrderSide.SELL, strength=0.7, strategy_name=self.name)
        
        return None
