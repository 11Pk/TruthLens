from pydantic import BaseModel
from typing import List


class AtomicClaim(BaseModel):
    claim: str
    source_sentence: str


class ClaimProcessingResult(BaseModel):
    claims: List[AtomicClaim]