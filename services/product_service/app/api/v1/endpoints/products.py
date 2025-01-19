from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.product import Product as ProductModel
from app.schemas.product import ProductCreate, Product as ProductResponse
from app.services.product_service import list_products, get_product, add_product
from app.db.base import AsyncSessionLocal

router = APIRouter()

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/products", response_model=List[ProductResponse])
async def get_products(search: str = None, category: str = None, db: AsyncSession = Depends(get_db)):
    query = select(ProductModel)
    
    if search:
        query = query.filter(ProductModel.name.ilike(f"%{search}%"))
    
    if category:
        query = query.filter(ProductModel.category == category)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/products/{product_id}", response_model=ProductResponse)
async def retrieve_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_product(product_id, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    product_model = ProductModel(**product.dict())  # Create SQLAlchemy model instance
    return await add_product(product_model, db) 