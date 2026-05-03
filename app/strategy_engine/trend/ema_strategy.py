# app/strategy_engine/trend/ema_strategy.py
import pandas as pd
import pandas_ta as ta
from typing import Optional
from app.strategy_engine.base_strategy import BaseStrategy
from app.core.types import Signal, OrderSide
from datetime import datetime

class EMAStrategy(BaseStrategy):
    def __init__(self, symbols: list, ema_period: int = 200):
        super().__init__("EMA_Trend_Strategy", symbols)
        self.ema_period = ema_period
        # Her sembol için geçmiş mumları tutan sözlük
        self.history = {symbol: [] for symbol in symbols}

    async def on_candle(self, candle: dict) -> Optional[Signal]:
        symbol = candle['symbol']
        self.history[symbol].append(candle)

        # Yeterli veri birikti mi?
        if len(self.history[symbol]) < self.ema_period:
            return None

        # Veriyi DataFrame'e çevir (Teknik analiz için)
        df = pd.DataFrame(self.history[symbol])
        
        # EMA hesapla
        ema = ta.ema(df['close'], length=self.ema_period)
        current_ema = ema.iloc[-1]
        current_close = df['close'].iloc[-1]
        prev_close = df['close'].iloc[-2]

        # STRATEJİ MANTIĞI: 
        # Fiyat EMA 200'ün üzerindeyse ve son mum yükselişle kapandıysa -> BUY
        if current_close > current_ema and current_close > prev_close:
            return Signal(
                symbol=symbol,
                side=OrderSide.BUY,
                strength=0.7, # Güç skoru
                strategy_name=self.name,
                metadata={"ema": current_ema, "close": current_close}
            )
        
        # Fiyat EMA 200'ün altındaysa ve son mum düşüşle kapandıysa -> SELL
        elif current_close < current_ema and current_close < prev_close:
            return Signal(
                symbol=symbol,
                side=OrderSide.SELL,
                strength=0.7,
                strategy_name=self.name,
                metadata={"ema": current_ema, "close": current_close}
            )

        return None
