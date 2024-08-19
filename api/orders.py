"""
@author: Yasir Khalid
To simulate CRUD for an inventory management system which also tracks payments made
"""

import os
from typing import Optional, Literal
from dotenv import load_dotenv
import httpx
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

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str = Literal["pending", "completed", "refunded"]

    class Meta:
        database = redis

class OrderCreationRequest(HashModel):
    product_id: str
    quantity: int

    class Meta:
        database = redis

@app.get("/")
async def default_landing_zone():
    """Description of the API that shows up in swagger UI"""
    return {"message": "Welcome to Orders/ microservice"}

def get_product_info(product_key: str):
    r = httpx.get(f'http://localhost:8000/products/{product_key}')
    return r.json()[0]

@app.get("/orders")
async def get_all_orders():
    """Using Query params, limit response or filter for ratings"""
    return Order.all_pks()

@app.post("/orders")
async def post_order(order_created: OrderCreationRequest):
    """CREATE ORDER AND FETCH METADATA AGAINST PRODUCT"""
    product_details = get_product_info(order_created.product_id)
    order = Order(
        product_id=order_created.product_id,
        price=product_details['price'],
        fee=0.10,
        total= product_details['price'] * 1.10 * order_created.quantity,
        quantity= order_created.quantity,
        status="completed"

    )
    order.save()
    return {
        "status": "ok",
        "order": dict(order)
    }


