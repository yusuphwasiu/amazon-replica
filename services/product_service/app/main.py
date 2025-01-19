import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.v1.endpoints import products
from app.db.base import engine
from app.models.product import Base
from app.kafka_producer import kafka_producer

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await kafka_producer.start()

@app.on_event("shutdown")
async def shutdown_event():
    await kafka_producer.stop()

app.include_router(products.router, prefix="/api/v1", tags=["products"])

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

import asyncio
asyncio.run(create_tables())