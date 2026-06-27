from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# Banco de dados em memória
db = {}
current_id = 1

# Modelo Pydantic com regras de validação
class Product(BaseModel):
    name: str = Field(..., min_length=2)
    price: float = Field(..., gt=0)

@app.post("/products/", status_code=201)
def create_product(product: Product):
    global current_id
    db[current_id] = product.model_dump()
    response = {"id": current_id, **db[current_id]}
    current_id += 1
    return response

@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"id": product_id, **db[product_id]}