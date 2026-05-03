# app/data_engine/ohlcv_builder.py
from datetime import datetime, timedelta
from app.core.event_bus import event_bus
from app.core.types import TickData
from app.core.logger import logger

class OHLCVBuilder:
    def __init__(self, timeframe_minutes: int = 1):
        self.tf = timeframe_minutes
        self.candles = {} # { 'BTCUSDT': {open, high, low, close, volume, timestamp} }

    async def on_tick(self, tick: TickData):
        symbol = tick.symbol
        
        # Mevcut zaman diliminin başlangıç vaktini hesapla (Örn: 14:05:00)
        timestamp = tick.timestamp
        candle_start = timestamp.replace(second=0, microsecond=0)
        if self.tf > 1:
            # Daha yüksek zaman dilimleri için yuvarlama (Örn: 5dk'lık mumlar)
            minute = (timestamp.minute // self.tf) * self.tf
            candle_start = timestamp.replace(minute=minute, second=0, microsecond=0)

        if symbol not in self.candles:
            self.candles[symbol] = self._create_new_candle(tick, candle_start)
            return

        current_candle = self.candles[symbol]

        # Eğer gelen tick yeni bir zaman dilimine aitse, eski mumu kapat ve yenisini aç
        if candle_start > current_candle['timestamp']:
            # MUM KAPATILDI -> Sinyal motoruna gönder
            await event_bus.publish("CANDLE_CLOSED", current_candle)
            
            # Yeni mumu başlat
            self.candles[symbol] = self._create_new_candle(tick, candle_start)
        else:
            # Mevcut mumu güncelle
            current_candle['high'] = max(current_candle['high'], tick.price)
            current_candle['low'] = min(current_candle['low'], tick.price)
            current_candle['close'] = tick.price
            current_candle['volume'] += tick.volume

    def _create_new_candle(self, tick, timestamp):
        return {
            "symbol": tick.symbol,
            "open": tick.price,
            "high": tick.price,
            "low": tick.price,
            "close": tick.price,
            "volume": tick.volume,
            "timestamp": timestamp
        }
