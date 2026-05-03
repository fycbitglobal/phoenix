# app/data_engine/orderbook_stream.py
import asyncio
import json
import websockets
from app.core.event_bus import event_bus
from app.core.logger import logger

class OrderbookStream:
    def __init__(self, symbols: list):
        self.symbols = symbols
        self.base_url = "wss://stream.binance.com:9443/ws"

    async def connect(self):
        # HATALI YER BURASIYDI: 'symbols' değil 'self.symbols' olmalı
        streams = [f"{s.lower()}@depth20@100ms" for s in self.symbols]
        subscribe_msg = {"method": "SUBSCRIBE", "params": streams, "id": 1}
        
        while True:
            try:
                async with websockets.connect(self.base_url) as websocket:
                    logger.info("Orderbook Stream bağlandı.")
                    await websocket.send(json.dumps(subscribe_msg))
                    while True:
                        message = await websocket.recv()
                        data = json.loads(message)
                        if "b" in data: 
                            await event_bus.publish("ORDERBOOK_UPDATE", data)
            except Exception as e:
                logger.error(f"Orderbook Hatası: {e}")
                await asyncio.sleep(5)
