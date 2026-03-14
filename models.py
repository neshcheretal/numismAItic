from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class LotData:
    url: str
    auction_house: str
    lot_id: Optional[str] = None

    title: Optional[str] = None
    seller: Optional[str] = None

    status: str = "unknown"  # active | sold | closed | unknown

    added_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None

    current_price_uah: Optional[float] = None
    final_price_uah: Optional[float] = None
    buy_now_price_uah: Optional[float] = None

    metal: Optional[str] = None
    material: Optional[str] = None
    condition_text: Optional[str] = None
    restoration: Optional[str] = None
    defects: Optional[str] = None
    location: Optional[str] = None
    payment: Optional[str] = None
    shipping: Optional[str] = None
    description: Optional[str] = None

    image_urls: List[str] = field(default_factory=list)


class SearchConfig(BaseModel):
    max_comparables: int
    min_comparables: int
    primary_mode: str
    fallback_mode: str
    fallback_year_delta: int
    penalize_year_distance: bool = True


class AgentConfig(BaseModel):
    role: str
    goal: str
    backstory: str
    llm: str
    verbose: bool = False
    allow_delegation: bool = False


class TaskConfig(BaseModel):
    description: str
    expected_output: str
