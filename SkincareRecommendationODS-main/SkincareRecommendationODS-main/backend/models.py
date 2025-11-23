from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class RecommendationRequest(BaseModel):
    ingredient: str
    top_n: int = 10  # Vai recomendar 10 produtos parecidos por ingredientes

class RecommendationResponse(BaseModel):
    results: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
