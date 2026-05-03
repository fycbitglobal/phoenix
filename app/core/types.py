# app/core/types.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from .constants import OrderSide, OrderType

class TickData(BaseModel):
    symbol: str
    price: float
    volume: float
    timestamp: datetime
    exchange: str

class Signal(BaseModel):
    symbol: str
    side: OrderSide
    strength: float  # 0.0 ile 1.0 arası (Skorlama için)
    strategy_name: str
    timestamp: datetime = datetime.now()
    metadata: Dict[str, Any] = {}

class OrderRequest(BaseModel):
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
