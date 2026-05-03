# app/execution_engine/retry_engine.py
import asyncio
from app.core.logger import logger

class RetryEngine:
    def __init__(self, max_retries: int = 3, delay: float = 1.0):
        self.max_retries = max_retries
        self.delay = delay

    async def execute(self, func, *args, **kwargs):
        """Bir fonksiyonu hata durumunda belirtilen sayıda tekrar dener."""
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                logger.warning(f"API Hatası: {e}. Deneme {attempt+1}/{self.max_retries}. {self.delay}sn bekleniyor...")
                await asyncio.sleep(self.delay)
        
        logger.error(f"Kritik API Hatası: {self.max_retries} deneme başarısız oldu.")
        raise last_exception
