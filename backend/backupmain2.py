from fastapi import FastAPI, HTTPException
from backend.models import RecommendationResponse, RecommendationRequest
from backend.recommender import recommend_by_ingredients
from backend.recommender import recommend_by_user
from pydantic import BaseModel, Field
import sys
import csv
import os

sys.stdout.reconfigure(encoding="utf-8")
CSV_FILE = r"data/more_ava.csv"
CSV_HEADERS = ["user_id", "product_id", "ranking"]

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

class Avaliacao(BaseModel):
    usuario: str
    produto: str
    avaliacao: int
@app.post("/avaliar")
def enviar_avaliacao(av: Avaliacao):
    nova_linha = Avaliacao.model_dump
    try:
        file_exists = os.path.isfile(CSV_FILE)
        
        with open(CSV_FILE, 'a+', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(nova_linha)

    except IOError as e:
        # Se houver um erro de escrita, lançamos uma exceção HTTP
        raise HTTPException(
            status_code=500, 
            detail=f"Não foi possível salvar a avaliação. Erro de I/O: {e}"
        )



class RecommendationUserRequest(BaseModel):
    username: str
    top_k_neighbors: int = 3
    top_n_products: int = 5

@app.post("/recommend_user", response_model=RecommendationResponse)
def recommend_user(request: RecommendationUserRequest):
    """
    Endpoint de recomendação colaborativa baseada em usuários
    """
    results_list = recommend_by_user(
    username=request.username, 
    top_k_neighbors=request.top_k_neighbors,
    top_n_products=request.top_n_products
)
    # Se não houver recomendação ou usuário não encontrado
    if isinstance(results_list, str):
        return {"error": results_list}

    # Converte lista de tuplas (produto, score) em lista de dicts
    results = [{"name": prod, "score": score} for prod, score in results_list]

    return {"results": results}
