from pydantic import BaseModel

class VerificationResult(BaseModel):
    verified: bool
    distance: float
    threshold: float
    model: str
    detector_backend: str