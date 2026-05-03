# app/execution_engine/order_router.py
from .binance_executor import BinanceExecutor
from app.core.types import OrderRequest
from app.core.logger import logger

class OrderRouter:
    def __init__(self):
        self.executors = {
            "Binance": BinanceExecutor(),
            # "Bybit": BybitExecutor() # İleride eklenebilir
        }

    async def route_order(self, order: OrderRequest, exchange_name: str = "Binance"):
        """Emri ilgili borsanın executor'ına yönlendirir."""
        executor = self.executors.get(exchange_name)
        if not executor:
            logger.error(f"Borsa {exchange_name} tanımlı değil!")
            return None
            
        logger.info(f"🚀 Emir {exchange_name} üzerinden yönlendiriliyor...")
        return await executor.place_order(order)

    async def shutdown(self):
        for exec in self.executors.values():
            await exec.close()
