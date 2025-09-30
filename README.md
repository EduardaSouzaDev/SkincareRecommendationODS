# 💆🏻‍♀️ Sistema de Recomendação de Skincare 🫧⋆｡˚

### Equipe: Eduarda Souza, Gustavo Almada, Rafael Santos.

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

Foi utilizada a similaridade de Pearson, pois:

 - Mede a proximidade considerando o rigor das avaliações dos usuários, ignorando a diferença aboluta entre algumas notas, e sim usando de avaliações anteriores para se basear no que pode ser considerado como uma avaliação de nota alta por um usuário X e o que pode ser consideradao nota Alta para um certo usuário Y.

 - É altamente eficaz em modelos de Filtragem Colaborativa Baseada em Usuário.

 - É mais eficiente porque percebe o comportamento de cada usuário e usa como parte da avaliação, e para um sistema de recomendação de cosméticos é muito útil, pois cosméticos tem muito peso com a experiência do usuário e seu emocional, que pontos técnicos dos produtos avaliados.

## Cálculo e análise da acurácia.
 - Segue abaixo uma tabela com os valores usados para teste da acurácia. Esse cálculo foi feito em um ambiente controlado, afim de demonstrar a eficácia do código, e que ele atende com os requisitos do escopo do projeto.

| Index | User | Hits | Recommended | Relevant | Accuracy | Precision | Recall |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | Fatima | 4 | 5 | 5 | 0.8 | 0.8 | 0.80 |
| 1 | Vitoria | 4 | 5 | 4 | 0.8 | 0.8 | 1.00 |
| 2 | Alex | 4 | 5 | 4 | 0.8 | 0.8 | 1.00 |
| 3 | Bia | 2 | 5 | 2 | 0.4 | 0.4 | 1.00 |
| 4 | Nazare | 2 | 5 | 2 | 0.4 | 0.4 | 1.00 |
| 5 | Sheila | 3 | 5 | 3 | 0.6 | 0.6 | 1.00 |

| Acurácia média: 63.33% |
| :---: |
| Precisão média: 63.33% |
| Recall médio: 92.50% |

- Podemos obersar que a acurácia média foi de, 63%, o que julgamos um bom valor, então mais da metade das recomendações foram acertivas.
- Tivemos um ótimo recall, que é a proporção de produtos relevantes, o valor chegou a 92%.
- E a nossa precição atigiu o valor, também de 63%, que é a proporção de produtos recomendados que foram relevantes.
