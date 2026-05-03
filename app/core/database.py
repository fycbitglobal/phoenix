# app/core/database.py
import aiosqlite
from app.core.logger import logger
import os

class Database:
    def __init__(self, db_path="trading_os.db"):
        self.db_path = db_path

    async def initialize(self):
        """Tabloları oluşturur."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # 1. Aktif Pozisyonlar Tablosu
                await db.execute('''
                    CREATE TABLE IF NOT EXISTS active_positions (
                        symbol TEXT PRIMARY KEY,
                        side TEXT,
                        entry_price REAL,
                        quantity REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 2. İşlem Geçmişi Tablosu
                await db.execute('''
                    CREATE TABLE IF NOT EXISTS trade_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        symbol TEXT,
                        side TEXT,
                        entry_price REAL,
                        exit_price REAL,
                        quantity REAL,
                        pnl REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                await db.commit()
                logger.info(f"✅ Veritabanı bağlandı ve tablolar hazır: {self.db_path}")
        except Exception as e:
            logger.error(f"❌ Veritabanı başlatma hatası: {e}")

    # --- Pozisyon İşlemleri ---
    async def save_position(self, symbol, side, entry, qty):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO active_positions (symbol, side, entry_price, quantity) VALUES (?, ?, ?, ?)",
                (symbol, side, entry, qty)
            )
            await db.commit()

    async def remove_position(self, symbol):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM active_positions WHERE symbol = ?", (symbol,))
            await db.commit()

    async def load_all_positions(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM active_positions") as cursor:
                rows = await cursor.fetchall()
                return {row[0]: {"side": row[1], "entry": row[2], "qty": row[3]} for row in rows}

    # --- İşlem Geçmişi İşlemleri ---
    async def log_trade(self, symbol, side, entry, exit, qty, pnl):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO trade_history (symbol, side, entry_price, exit_price, quantity, pnl) VALUES (?, ?, ?, ?, ?, ?)",
                (symbol, side, entry, exit, qty, pnl)
            )
            await db.commit()

    async def get_total_pnl(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT SUM(pnl) FROM trade_history") as cursor:
                row = await cursor.fetchone()
                return row[0] if row[0] else 0.0

# Singleton yapısı
db = Database()
