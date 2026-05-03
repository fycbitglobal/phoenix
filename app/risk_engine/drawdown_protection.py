# app/risk_engine/drawdown_protection.py
from app.core.logger import logger

class DrawdownProtection:
    def __init__(self, max_daily_loss_percent: float = 0.05): # Günlük %5 kayıpta dur
        self.max_daily_loss = max_daily_loss_percent
        self.initial_balance = 0.0

    def check_drawdown(self, current_balance: float) -> bool:
        """Kasa kaybı limitleri aşmış mı kontrol eder."""
        if self.initial_balance == 0:
            self.initial_balance = current_balance
            return True
        
        drawdown = (self.initial_balance - current_balance) / self.initial_balance
        if drawdown > self.max_daily_loss:
            logger.error(f"🛑 CRITICAL: Günlük kayıp limiti (%{self.max_daily_loss*100}) aşıldı! İşlemler durduruldu.")
            return False
        return True
