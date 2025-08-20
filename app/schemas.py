 
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict

class MatchRequest(BaseModel):
    location: Optional[str] = None
    property_types: Optional[List[str]] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    min_bed: Optional[int] = None
    min_bath: Optional[float] = None
    min_cap_rate: Optional[float] = None
    strategy: Optional[Literal["buy_and_hold", "short_term_rental", "flip"]] = "buy_and_hold"
    n_results: int = 5
    preference_text: Optional[str] = None

class PropertyOut(BaseModel):
    id: str
    address: str
    city: str
    state: str
    price: float
    beds: int
    baths: float
    sqft: int
    property_type: str
    cap_rate: float
    noi_annual: float
    roi_cash_on_cash: float
    avm_price: float
    score: float

class MatchResponse(BaseModel):
    results: List[PropertyOut]
    meta: Dict[str, float] = Field(default_factory=dict)

class ReportRequest(BaseModel):
    property_ids: List[str]
    investor_name: str
    preferences_summary: Optional[str] = None

class ReportResponse(BaseModel):
    markdown: str
