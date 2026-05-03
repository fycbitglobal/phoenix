# app/signal_engine/signal_filter.py
from app.signal_engine.signal_model import FusedSignal

class SignalFilter:
    def __init__(self, min_score: float = 0.5):
        self.min_score = min_score

    def is_valid(self, fused_signal: FusedSignal) -> bool:
        # 1. Skor eşiği kontrolü
        if fused_signal.final_score < self.min_score:
            return False
        
        # 2. Çok az strateji onay verdiyse reddet (Örn: Sadece 1 strateji yetmez)
        if len(fused_signal.contributing_strategies) < 2:
            return False
            
        return True
