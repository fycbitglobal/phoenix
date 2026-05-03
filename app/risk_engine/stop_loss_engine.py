# app/risk_engine/stop_loss_engine.py
from app.core.types import OrderSide

class StopLossEngine:
    def __init__(self, default_risk_reward: float = 2.0):
        self.rr_ratio = default_risk_reward # 1:2 Risk Ödül Oranı

    def calculate_sl_tp(self, side: OrderSide, entry_price: float, volatility: float = None):
        """
        Sinyal yönüne göre Stop-Loss ve Take-Profit seviyelerini belirler.
        Sadeleştirilmiş versiyon: Volatilite (ATR) yoksa %1 stop kullanılır.
        """
        sl_percent = 0.01 # %1 Stop Loss
        
        if side == OrderSide.BUY:
            sl = entry_price * (1 - sl_percent)
            risk = entry_price - sl
            tp = entry_price + (risk * self.rr_ratio)
        else:
            sl = entry_price * (1 + sl_percent)
            risk = sl - entry_price
            tp = entry_price - (risk * self.rr_ratio)
            
        return sl, tp
