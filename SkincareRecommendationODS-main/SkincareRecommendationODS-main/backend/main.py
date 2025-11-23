from fastapi import FastAPI, HTTPException
from backend.models import RecommendationResponse, RecommendationRequest
from backend.recommender import recommend_by_ingredients
from backend.recommender import recommend_by_user
from pydantic import BaseModel, Field
import sys
import csv
import os

sys.stdout.reconfigure(encoding="utf-8")
CSV_FILE = r"backend/data/more_ava.csv"
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
    print(f"Recebido: usuario={av.usuario}, produto={av.produto}, avaliacao={av.avaliacao}")
<<<<<<< HEAD
    with open(r"backend/data/more_ava.cs", "a", newline="", encoding="utf-8") as f:
=======
    with open("backend\data\more_ava.csv", "a", newline="", encoding="utf-8") as f:
>>>>>>> 9e5e0999a6d3deb99f65b5b88aa56987936a4eaa
        writer = csv.writer(f)
        writer.writerow([av.usuario, av.produto, av.avaliacao])
    return {"status": "sucesso", "mensagem": "Avaliação registrada!"}



class RecommendationUserRequest(BaseModel):
    username: str
    top_k_neighbors: int = 3
    top_n_products: int = 5

@app.post("/recommend_user")
def recommend_user(request: RecommendationUserRequest):
<<<<<<< HEAD
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

=======
    results = recommend_by_user(
        username=request.username,
        top_k_neighbors=request.top_k_neighbors,
        top_n_products=request.top_n_products
    )
    if isinstance(results, str):
        return {"error": results}
    # results já é lista de dicts com name,brand,ingredients,price,score
>>>>>>> 9e5e0999a6d3deb99f65b5b88aa56987936a4eaa
    return {"results": results}
