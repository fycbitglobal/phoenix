# app/monitoring/pnl_tracker.py
from app.core.logger import logger
from app.core.database import db

class PNLTracker:
    def __init__(self):
        self.total_realized_pnl = 0.0
        self.total_trades = 0
        self.wins = 0
        self.losses = 0

    async def sync_with_db(self):
        """Veritabanındaki tüm geçmişten PNL ve istatistikleri hesapla."""
        self.total_realized_pnl = await db.get_total_pnl()
        # Detaylı istatistikler için trade_history tablosunu sorgulayabiliriz
        logger.info(f"📊 PNL Senkronize Edildi. Mevcut Toplam: {self.total_realized_pnl:.2f}")

    def update_pnl(self, pnl: float):
        self.total_realized_pnl += pnl
        self.total_trades += 1
        if pnl > 0: self.wins += 1
        else: self.losses += 1

    def get_stats(self):
        return {
            "total_pnl": self.total_realized_pnl,
            "trades": self.total_trades,
            "win_rate": (self.wins / self.total_trades * 100) if self.total_trades > 0 else 0
        }
