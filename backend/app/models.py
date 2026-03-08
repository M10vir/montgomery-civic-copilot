from typing import List
from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    intent: str
    matched_record_id: str
    matched_title: str
    answer: str
    recommended_service: str
    next_steps: List[str]
    source_label: str
    source_url: str
    confidence: float

class AskLiveRequest(BaseModel):
    question: str

class AskLiveResponse(BaseModel):
    intent: str
    matched_record_id: str
    matched_title: str

    trusted_answer: str
    live_insights: List[str]
    final_answer: str

    recommended_service: str
    next_steps: List[str]
    sources: List[str]
    confidence: float
    live_mode: str
    live_debug: str

class AddressLookupRequest(BaseModel):
    address: str

class AddressLookupResponse(BaseModel):
    address: str
    district: str
    representative: str
    source_label: str
    source_url: str
    confidence: float

class HealthResponse(BaseModel):
    status: str
    app: str
    version: str

class EnrichRequest(BaseModel):
    query: str

class EnrichResponse(BaseModel):
    url: str
    status: str
    content: str
    source_label: str
