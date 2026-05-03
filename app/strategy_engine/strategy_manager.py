# app/strategy_engine/strategy_manager.py
from app.core.event_bus import event_bus
from app.core.logger import logger
from typing import List
from app.strategy_engine.base_strategy import BaseStrategy

class StrategyManager:
    def __init__(self):
        self.strategies: List[BaseStrategy] = []

    def add_strategy(self, strategy: BaseStrategy):
        self.strategies.append(strategy)
        logger.info(f"Strateji eklendi: {strategy.name}")

    async def on_candle_closed(self, candle: dict):
        """Mum kapandığında tüm stratejileri çalıştırır."""
        for strategy in self.strategies:
            try:
                signal = await strategy.on_candle(candle)
                if signal:
                    logger.info(f"🎯 SİNYAL OLUŞTU: {strategy.name} | {signal.symbol} | {signal.side}")
                    # Sinyali yayınla -> Artık Risk Engine bunu yakalayabilir
                    await event_bus.publish("SIGNAL_GENERATED", signal)
            except Exception as e:
                logger.error(f"Strateji hatası ({strategy.name}): {e}")

