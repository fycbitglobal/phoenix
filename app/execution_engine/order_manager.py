# app/execution_engine/order_manager.py
from app.core.logger import logger
from app.core.database import db

class OrderManager:
    def __init__(self):
        self.active_positions = {}

    async def load_positions_from_db(self):
        """Sistem açıldığında veritabanından pozisyonları yükle."""
        self.active_positions = await db.load_all_positions()
        logger.info(f"📦 Veritabanından {len(self.active_positions)} pozisyon yüklendi.")

    async def update_position(self, symbol, side, entry, qty):
        # 1. RAM'e ekle
        self.active_positions[symbol] = {
            "side": side,
            "entry": entry,
            "qty": qty
        }
        # 2. Veritabanına kaydet
        await db.save_position(symbol, side, entry, qty)
        logger.info(f"📦 Pozisyon Kaydedildi: {symbol} | {side} | {qty}")

    async def remove_position(self, symbol):
        if symbol in self.active_positions:
            del self.active_positions[symbol]
            await db.remove_position(symbol)
            logger.info(f"📦 Pozisyon Silindi: {symbol}")
