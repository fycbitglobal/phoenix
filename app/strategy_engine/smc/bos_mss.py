# app/strategy_engine/smc/bos_mss.py
import pandas as pd
from app.strategy_engine.base_strategy import BaseStrategy
from app.core.types import Signal, OrderSide
from typing import Optional

class BOSStrategy(BaseStrategy):
    def __init__(self, symbols: list):
        super().__init__("SMC_BOS_MSS_Strategy", symbols)
        self.history = {symbol: [] for symbol in symbols}
        self.last_high = {symbol: 0.0 for symbol in symbols}
        self.last_low = {symbol: float('inf') for symbol in symbols}

    async def on_candle(self, candle: dict) -> Optional[Signal]:
        symbol = candle['symbol']
        self.history[symbol].append(candle)
        
        current_high = candle['high']
        current_low = candle['low']
        current_close = candle['close']

        # Zirve ve Dip Güncelleme (Basit Swing High/Low)
        if current_high > self.last_high[symbol]:
            self.last_high[symbol] = current_high
        if current_low < self.last_low[symbol]:
            self.last_low[symbol] = current_low

        # --- Market Structure Shift (MSS) ---
        # Fiyat önceki zirveyi yukarıyla kapattıysa -> Yükselen Trend Başladı (BOS)
        if current_close > self.last_high[symbol] * 1.0005: 
            return Signal(
                symbol=symbol,
                side=OrderSide.BUY,
                strength=0.9, # Yapı kırılımı çok güçlü bir sinyaldir
                strategy_name=self.name,
                metadata={"event": "BOS_BULLISH"}
            )

        # Fiyat önceki dibi aşağıyla kapattıysa -> Düşen Trend Başladı (BOS)
        if current_close < self.last_low[symbol] * 0.9995:
            return Signal(
                symbol=symbol,
                side=OrderSide.SELL,
                strength=0.9,
                strategy_name=self.name,
                metadata={"event": "BOS_BEARISH"}
            )

        return None
