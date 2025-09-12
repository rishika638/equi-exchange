from sqlmodel import SQLModel, Field
from typing import Optional
import datetime

class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str  # 'buyer' or 'seller' requesting session
    buyer_address: Optional[str] = None
    seller_address: Optional[str] = None
    target_price: Optional[float] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    quantity: Optional[int] = None
    fairness_weight: Optional[float] = 0.5
    max_rounds: Optional[int] = 8
    status: str = "open"
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class Offer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int
    round: int
    made_by: str
    price: float
    quantity: int
    fairness: float
    utility: float
    payload: Optional[str] = None

class Agreement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int
    price: float
    quantity: int
    agreement_hash: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
