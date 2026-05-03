# app/signal_engine/signal_model.py
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
from app.core.types import OrderSide

class FusedSignal(BaseModel):
    symbol: str
    side: OrderSide  # <--- BURASI ÇOK KRİTİK, EKLEMİŞ OLDUK
    final_score: float
    contributing_strategies: List[str]
    timestamp: datetime = datetime.now()
    confidence_level: str
    metadata: Dict[str, Any] = {}
