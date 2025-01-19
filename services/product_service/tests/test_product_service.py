import pytest
from fastapi.testclient import TestClient
from app.main import app  # Assuming your FastAPI app is defined in app.main

client = TestClient(app)

@pytest.fixture
def sample_product():
    return {
        "name": "Sample Product",
        "description": "This is a sample product.",
        "price": 19.99,
        "inventory": 100,
        "category": "Sample Category"
    }

def test_list_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product_details():
    response = client.get("/products/1")  # Assuming product with ID 1 exists
    assert response.status_code == 200
    assert "name" in response.json()

def test_add_product(sample_product):
    response = client.post("/products", json=sample_product)
    assert response.status_code == 201
    assert response.json()["name"] == sample_product["name"]

def test_search_products_by_name():
    response = client.get("/products?search=Sample")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_filter_products_by_category():
    response = client.get("/products?category=Sample Category")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_filter_products_by_price():
    response = client.get("/products?min_price=10&max_price=20")
    assert response.status_code == 200
    assert all(product["price"] >= 10 and product["price"] <= 20 for product in response.json())

def test_filter_products_by_rating():
    response = client.get("/products?min_rating=4")
    assert response.status_code == 200
    assert all(product["rating"] >= 4 for product in response.json())

def test_similar_product_suggestions():
    response = client.get("/products/1/similar")  # Assuming product with ID 1 exists
    assert response.status_code == 200
    assert len(response.json()) > 0 