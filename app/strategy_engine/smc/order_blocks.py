# app/strategy_engine/smc/order_blocks.py
import pandas as pd
from app.strategy_engine.base_strategy import BaseStrategy
from app.core.types import Signal, OrderSide
from typing import Optional

class OrderBlockStrategy(BaseStrategy):
    def __init__(self, symbols: list):
        super().__init__("SMC_OrderBlock_Strategy", symbols)
        self.history = {symbol: [] for symbol in symbols}

    async def on_candle(self, candle: dict) -> Optional[Signal]:
        symbol = candle['symbol']
        self.history[symbol].append(candle)
        if len(self.history[symbol]) < 5: return None

        df = pd.DataFrame(self.history[symbol])
        
        # Basit OB Mantığı: 
        # Eğer fiyat sert bir şekilde yükseldiyse (Impulse), 
        # yükselişten önceki son düşüş mumuna bak.
        
        last_candle = df.iloc[-1]
        prev_candle = df.iloc[-2]
        
        # Bullish OB: Son mum güçlü bir yükseliş mumuysa, önceki mum düşüş mumu olmalı
        if last_candle['close'] > prev_candle['high'] * 1.001: # %0.1'lik sert hareket
            if prev_candle['close'] < prev_candle['open']: # Önceki mum kırmızı (düşüş)
                return Signal(
                    symbol=symbol,
                    side=OrderSide.BUY,
                    strength=0.8,
                    strategy_name=self.name,
                    metadata={"ob_zone": (prev_candle['low'], prev_candle['high'])}
                )

        # Bearish OB: Son mum güçlü bir düşüş mumuysa, önceki mum yükseliş mumu olmalı
        if last_candle['close'] < prev_candle['low'] * 0.999:
            if prev_candle['close'] > prev_candle['open']: # Önceki mum yeşil (yükseliş)
                return Signal(
                    symbol=symbol,
                    side=OrderSide.SELL,
                    strength=0.8,
                    strategy_name=self.name,
                    metadata={"ob_zone": (prev_candle['low'], prev_candle['high'])}
                )

        return None
