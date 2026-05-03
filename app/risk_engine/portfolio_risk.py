# app/risk_engine/portfolio_risk.py

class PortfolioRisk:
    def __init__(self, max_open_positions: int = 3):
        self.max_open_positions = max_open_positions
        self.current_positions = 0

    def can_open_new_position(self) -> bool:
        """Toplam açık pozisyon sayısını kontrol eder."""
        return self.current_positions < self.max_open_positions

    def update_position_count(self, count: int):
        self.current_positions = count
