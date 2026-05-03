# app/strategy_engine/base_strategy.py
from abc import ABC, abstractmethod
from app.core.types import Signal
from typing import Optional

class BaseStrategy(ABC):
    def __init__(self, name: str, symbols: list):
        self.name = name
        self.symbols = symbols

    @abstractmethod
    async def on_candle(self, candle: dict) -> Optional[Signal]:
        """
        Her yeni mum kapandığında bu metod çağrılır.
        Eğer strateji bir sinyal üretiyorsa Signal objesi döner, yoksa None döner.
        """
        pass
