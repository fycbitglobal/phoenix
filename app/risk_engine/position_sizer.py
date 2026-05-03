# app/risk_engine/position_sizer.py
from app.core.config import settings
from app.core.types import OrderRequest

class PositionSizer:
    def __init__(self, risk_per_trade: float = 0.01): # Her işlemde kasanın %1'i risk edilir
        self.risk_per_trade = risk_per_trade

    def calculate_size(self, balance: float, entry_price: float, stop_loss: float) -> float:
        """
        Kasa bakiyesine ve Stop-Loss mesafesine göre girilecek lot miktarını hesaplar.
        Formül: Miktar = (Kasa * Risk%) / (Giriş - StopLoss)
        """
        risk_amount = balance * self.risk_per_trade
        price_diff = abs(entry_price - stop_loss)
        
        if price_diff == 0: return 0.0
        
        quantity = risk_amount / price_diff
        return quantity
