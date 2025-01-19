from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    inventory: int
    category: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True 