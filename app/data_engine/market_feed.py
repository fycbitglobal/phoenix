# app/data_engine/market_feed.py
import asyncio
from .binance_ws import BinanceWS
from .ohlcv_builder import OHLCVBuilder
from app.core.event_bus import event_bus
from app.core.logger import logger

class MarketFeed:
    def __init__(self, symbols: list):
        self.symbols = symbols
        self.binance_ws = BinanceWS(symbols)
        self.ohlcv_builder = OHLCVBuilder(timeframe_minutes=1) # 1 dakikalık mumlar

    async def start(self):
        logger.info("Market Feed başlatılıyor...")

        # OHLCV Builder'ı Tick olayına abone yap
        event_bus.subscribe("TICK_RECEIVED", self.ohlcv_builder.on_tick)

        # Binance bağlantısını başlat
        await asyncio.gather(
            self.binance_ws.connect(),
            # Buraya ileride bybit_ws.connect() eklenecek
        )
