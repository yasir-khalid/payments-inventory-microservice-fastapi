"""
@author: Yasir Khalid
To simulate CRUD for an inventory management system which also tracks payments made
"""

import os
from typing import Optional
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

# Load environment variables from the .env file (if present)
load_dotenv()

app = FastAPI()
"""FastAPI runs through the code top to bottom and prioritses API logic based
on the function that appears first
"""
# Add CORS middleware to allow all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

redis = get_redis_connection(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

@app.get("/")
async def default_landing_zone():
    """Description of the API that shows up in swagger UI"""
    return {"message": "Welcome to Products/ microservice"}

def get_product_info(product_key):
    product = Product.get(product_key)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.get("/products")
async def get_all_products():
    """Using Query params, limit response or filter for ratings"""
    return [get_product_info(product_key) for product_key in Product.all_pks()]

@app.get("/products/{product_key}")
async def get_product(product_key: str):
    """Using Query params, limit response or filter for ratings"""
    return [get_product_info(product_key)]

@app.post('/products')
async def create_product(product: Product):
    return product.save()


@app.delete('/products/{product_key}')
def delete_products(product_key: str):
    return Product.delete(product_key)