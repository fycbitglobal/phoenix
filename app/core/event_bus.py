# app/core/event_bus.py
import asyncio
from typing import Callable, Dict, List, Any
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class EventBus:
    def __init__(self):
        # Her event tipi için bir liste şeklinde callback fonksiyonları tutar
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, callback: Callable):
        """Bir fonksiyonu belirli bir event tipine abone yapar."""
        self._subscribers[event_type].append(callback)
        logger.info(f"Sisteme abone olundu: {event_type} -> {callback.__name__}")

    async def publish(self, event_type: str, data: Any):
        """Belirli bir event tipindeki tüm abonelere veriyi gönderir."""
        if event_type not in self._subscribers:
            return

        tasks = []
        for callback in self._subscribers[event_type]:
            # Callback'lerin asenkron olduğunu varsayıyoruz
            tasks.append(asyncio.create_task(callback(data)))
        
        if tasks:
            await asyncio.gather(*tasks)

# Singleton yapısı: Tüm uygulama boyunca tek bir EventBus kullanılır
event_bus = EventBus()
