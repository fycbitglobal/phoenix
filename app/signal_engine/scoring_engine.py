# app/signal_engine/scoring_engine.py
from app.core.types import Signal

class ScoringEngine:
    def __init__(self):
        # Strateji ağırlıkları (Toplamı 1.0 olması gerekmez, skorlama için kullanılır)
        self.weights = {
            "SMC_BOS_MSS_Strategy": 0.4,    # Yapı kırılımı en güçlüsü
            "SMC_OrderBlock_Strategy": 0.3, # Kurumsal bölgeler çok değerli
            "SMC_LiqSweep_Strategy": 0.3,  # Likidite temizliği değerli
            "SMC_FVG_Strategy": 0.2,        # FVG destekleyici
            "Volatility_Squeeze": 0.2,      # Patlama onayı
            "Trend_ADX": 0.1,               # Trend gücü onaylayıcı
            "Momentum_MACD": 0.1,           # Momentum onaylayıcı
            "MeanRev_Bollinger": 0.1,       # Tersine dönüş onayı
            "Trend_EMA": 0.05,              # Genel yön belirleyici
            "OrderFlow_Whale": 0.2          # Balina takibi
        }

    def calculate_score(self, signals: list[Signal]) -> float:
        """
        Gelen sinyalleri ağırlıklarına göre puanlar.
        """
        total_score = 0.0
        
        for sig in signals:
            weight = self.weights.get(sig.strategy_name, 0.05) # Tanımsızsa düşük ağırlık ver
            # Stratejinin kendi gücü (strength) * Stratejinin sistemdeki ağırlığı (weight)
            total_score += (sig.strength * weight)
            
        return min(total_score, 1.0) # Skor 1.0'ı geçmesin
