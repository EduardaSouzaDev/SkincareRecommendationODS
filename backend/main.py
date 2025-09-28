from fastapi import FastAPI
from backend.models import RecommendationResponse, RecommendationRequest
from backend.recommender import recommend_by_ingredients
import sys

sys.stdout.reconfigure(encoding="utf-8")

app = FastAPI(
    title="Skincare Recommendation API ",
    description="Serve recomendação de produtos de skincare da Sephora.",
    version="1.0.0"
)

# Saude da API
@app.get("/health", tags=["status"])
def health() -> dict:
    '''Endpoint de verificação de saúde da API'''
    return {"status": "ok"}

# Por ingredientes
@app.post("/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest): 
    '''Endpoint de recomendação por ingredientes'''
    
    results_df = recommend_by_ingredients(request.ingredient)

    if isinstance(results_df, str):  # caso retorne mensagem de erro
        return {"error": results_df}
    
    # Converte DataFrame para lista de dicts para JSON
    results = results_df.to_dict(orient="records")
    
    return {"results": results}
