from fastapi import FastAPI
from app.api.v1.endpoints import products
from app.db.base import engine
from app.models.product import Base

app = FastAPI()

app.include_router(products.router, prefix="/api/v1", tags=["products"])

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

import asyncio
asyncio.run(create_tables())