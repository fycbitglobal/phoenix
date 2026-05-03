# app/execution_engine/binance_executor.py
import ccxt.async_support as ccxt
from app.core.config import settings
from app.core.types import OrderRequest
from app.core.logger import logger
from .retry_engine import RetryEngine

class BinanceExecutor:
    def __init__(self):
        self.exchange = ccxt.binance({
            'apiKey': settings.BINANCE_API_KEY,
            'secret': settings.BINANCE_API_SECRET,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'} # Futures piyasası
        })
        self.retry = RetryEngine()

    async def place_order(self, order: OrderRequest):
        """Gerçek emri borsaya iletir."""
        # SİSTEM MODU KONTROLÜ (Paper/Live)
        if settings.SISTEM_MODU == "PAPER":
            logger.info(f"📝 [PAPER MODE] Binance'e emir gönderildi: {order.symbol} {order.side} {order.quantity}")
            return {"id": "sim_123", "status": "filled", "price": order.price}

        try:
            # Emri RetryEngine üzerinden gönder
            params = {'stopLoss': order.stop_loss, 'takeProfit': order.take_profit}
            result = await self.retry.execute(
                self.exchange.create_order, 
                order.symbol, 
                order.order_type.value.lower(), 
                order.side.value.lower(), 
                order.quantity, 
                order.price, 
                params
            )
            return result
        except Exception as e:
            logger.error(f"Binance Emir Hatası: {e}")
            return None

    async def close(self):
        await self.exchange.close()
