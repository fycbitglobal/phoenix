# app/api/main.py
from fastapi import FastAPI
from app.core.database import db
import aiosqlite
import asyncio

app = FastAPI(title="MTO Trading OS API")

@app.get("/")
async def root():
    return {"status": "Sistem Aktif", "version": "1.1.0"}

@app.get("/positions")
async def get_positions():
    async with aiosqlite.connect("trading_os.db") as conn:
        async with conn.execute("SELECT * FROM active_positions") as cursor:
            rows = await cursor.fetchall()
            return [{"symbol": r[0], "side": r[1], "entry": r[2], "qty": r[3]} for r in rows]

@app.get("/pnl")
async def get_pnl():
    async with aiosqlite.connect("trading_os.db") as conn:
        async with conn.execute("SELECT SUM(pnl) FROM trade_history") as cursor:
            row = await cursor.fetchone()
            return {"total_pnl": row[0] if row[0] else 0.0}

@app.get("/history")
async def get_history():
    async with aiosqlite.connect("trading_os.db") as conn:
        async with conn.execute("SELECT * FROM trade_//trade_history ORDER BY timestamp DESC LIMIT 50") as cursor:
            # Yazım hatası düzeltildi
            async with conn.execute("SELECT * FROM trade_history ORDER BY timestamp DESC LIMIT 50") as cursor:
                rows = await cursor.fetchall()
                return [{"id": r[0], "symbol": r[1], "side": r[2], "entry": r[3], "exit": r[4], "pnl": r[6]} for r in rows]

# YENİ: Dashboard için anlık fiyat endpoint'i (Simülasyon veya API'den çekilebilir)
@app.get("/price/{symbol}")
async def get_price(symbol: str):
    # Gerçek sistemde burası Binance API'ye bağlanır. 
    # Şimdilik sistemin çalıştığını görmek için rastgele küçük değişimli fiyat döner.
    import random
    return {"symbol": symbol, "price": 60000 + random.uniform(-100, 100)}

