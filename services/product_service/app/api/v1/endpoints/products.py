from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.services.product_service import list_products, get_product, add_product
from app.db.base import AsyncSessionLocal

router = APIRouter()

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/products", response_model=List[Product])
async def get_products(db: AsyncSession = Depends(get_db)):
    return await list_products(db)

@router.get("/products/{product_id}", response_model=Product)
async def retrieve_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_product(product_id, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products", response_model=Product)
async def create_product(product: Product, db: AsyncSession = Depends(get_db)):
    return await add_product(product, db) 