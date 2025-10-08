from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class Evidence(BaseModel):
    text: str
    title: str
    url: Optional[str] = None
    source: str  # domain like wikipedia.org, nytimes.com
    provider: str  # wikipedia|web|rss
    published: Optional[datetime] = None
    retrieved: datetime
    extra: Dict[str, str] = {}

class Claim(BaseModel):
    sentence: str
    support_evidence_idx: List[int]  # indices into Evidence list
    label: str  # Verified | Uncertain | Unverifiable
    notes: Optional[str] = None
    score: float = 0.0  # similarity/consensus score

class AskResponse(BaseModel):
    query: str
    answer: str
    claims: List[Claim]
    evidence: List[Evidence]
    valid_as_of: datetime
    decision_record_path: Optional[str] = None
