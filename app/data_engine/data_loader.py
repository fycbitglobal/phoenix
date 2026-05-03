# app/data_engine/data_loader.py
import asyncio
import ccxt.async_support as ccxt
from app.core.config import settings
from app.core.logger import logger
from datetime import datetime

class DataLoader:
    def __init__(self):
        self.exchange = ccxt.binance({
            'apiKey': settings.BINANCE_API_KEY,
            'secret': settings.BINANCE_API_SECRET,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })

    async def fetch_historical_candles(self, symbol: str, timeframe: str = '1m', limit: int = 500): # <--- BURAYI 500 YAPTIK
        """
        Borsadan geçmiş mum verilerini çeker.
        """
        try:
            logger.info(f"⏳ {symbol} için geçmiş veriler çekiliyor ({timeframe}, {limit} mum)...")
            # CCXT fetch_ohlcv ile verileri çek
            ohlcv = await self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            
            formatted_candles = []
            for c in ohlcv:
                formatted_candles.append({
                    "symbol": symbol,
                    "timestamp": datetime.fromtimestamp(c[0] / 1000.0),
                    "open": float(c[1]),
                    "high": float(c[2]),
                    "low": float(c[3]),
                    "close": float(c[4]),
                    "volume": float(c[5])
                })
            
            logger.info(f"✅ {symbol} için {len(formatted_candles)} mum başarıyla yüklendi.")
            return formatted_candles
        except Exception as e:
            logger.error(f"❌ {symbol} veri yükleme hatası: {e}")
            return []

    async def close(self):
        await self.exchange.close()
