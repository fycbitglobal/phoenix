# app/data_engine/binance_ws.py
import asyncio
import json
import websockets
from datetime import datetime
from app.core.event_bus import event_bus
from app.core.types import TickData
from app.core.logger import logger

class BinanceWS:
    def __init__(self, symbols: list):
        self.symbols = symbols
        # Binance Trade stream URL'i (AggTrade: Agrega edilmiş işlemler)
        self.base_url = "wss://stream.binance.com:9443/ws"
        self.streams = [f"{s.lower()}@aggTrade" for s in symbols]

    async def connect(self):
        # Birden fazla stream için tek bir bağlantı kuruyoruz
        subscribe_msg = {
            "method": "SUBSCRIBE",
            "params": self.streams,
            "id": 1
        }
        
        # Bağlantı yönetimi ve otomatik yeniden bağlanma (reconnect) döngüsü
        while True:
            try:
                async with websockets.connect(self.base_url) as websocket:
                    logger.info(f"Binance WebSocket bağlantısı kuruldu. Takip edilenler: {self.symbols}")
                    await websocket.send(json.dumps(subscribe_msg))

                    while True:
                        message = await websocket.recv()
                        data = json.loads(message)
                        
                        # Sadece trade verilerini işle (subscribe yanıtlarını atla)
                        if "s" in data: 
                            tick = TickData(
                                symbol=data['s'],
                                price=float(data['p']),
                                volume=float(data['q']),
                                timestamp=datetime.fromtimestamp(data['E'] / 1000.0),
                                exchange="Binance"
                            )
                            # VERİYİ YAYINLA: Artık tüm sistem bu tick'ten haberdar olabilir
                            await event_bus.publish("TICK_RECEIVED", tick)

            except Exception as e:
                logger.error(f"Binance WS Hatası: {e}. 5 saniye sonra yeniden bağlanılıyor...")
                await asyncio.sleep(5)
