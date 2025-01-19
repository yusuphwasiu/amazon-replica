from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.product import Product

# In-memory product storage for demonstration purposes
products_db = []

async def list_products(db: AsyncSession) -> List[Product]:
    result = await db.execute(select(Product))
    return result.scalars().all()

async def get_product(product_id: int, db: AsyncSession) -> Product:
    result = await db.execute(select(Product).filter(Product.id == product_id))
    return result.scalar_one_or_none()

async def add_product(product: Product, db: AsyncSession) -> Product:
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product 