# 💆🏻‍♀️ Sistema de Recomendação de Skincare 🫧⋆｡˚

## Objetivo do Sistema  
O sistema tem como objetivo **recomendar produtos de skincare similares com base em seus ingredientes**.  
Dado o nome de um produto, o sistema analisa os ingredientes cadastrados em um dataset e retorna aqueles com **maior similaridade de composição**.  

Essa abordagem auxilia consumidores e profissionais da área a **descobrir alternativas de produtos** com formulações parecidas, promovendo escolhas mais informadas e acessíveis.

---

## Estrutura dos Entregáveis  
- **Frontend:** desenvolvido com [Streamlit](https://streamlit.io/), responsável pela interface de interação do usuário.  
- **Backend:** desenvolvido com [FastAPI](https://fastapi.tiangolo.com/), responsável por processar as requisições e retornar recomendações.  
- **Dataset (.csv):** contém os produtos, marcas e ingredientes utilizados como base para cálculo da similaridade.  

---

##  Como Executar o Sistema  

###  1. Clonar o projeto  

git clone <URL_DO_REPOSITORIO>
cd <PASTA_DO_PROJETO>

### 2. Criar e ativar um ambiente virtual

python -m venv venv
venv\Scripts\activate    # No Windows
# ou
source venv/bin/activate # No Linux/Mac

### 3. Instalar dependências

pip install -r requirements.txt

### 4. Executar o backend (API)

No diretório do backend (onde está o arquivo main.py):

uvicorn main:app --reload

A API ficará disponível em: http://127.0.0.1:8000

### 5. Executar o frontend (Streamlit)

No diretório do frontend (onde está o arquivo app.py):

streamlit run app.py

A interface abrirá automaticamente no navegador (geralmente em http://localhost:8501).

## Justificativa da Métrica de Similaridade

Foi utilizada a similaridade do cosseno, pois:

 - Mede a proximidade angular entre vetores, desconsiderando magnitude — ideal para dados binários (presença/ausência de ingrediente).

 - É amplamente utilizada em sistemas de recomendação baseados em conteúdo.

 - É mais adequada que distâncias como Euclidiana, já que o objetivo é identificar proporção de interseção de ingredientes, e não diferenças absolutas.

Em resumo, o cosseno permite mensurar quão parecidos são dois produtos na formulação, o que é essencial neste domínio.
