"""Steps for loading BDD test data."""
import requests
from behave import given

BASE_URL = "http://127.0.0.1:5000"


@given("the following products")
def step_impl(context):
    """Load background products via the REST API"""
    for row in context.table:
        payload = {
            "name": row["name"],
            "category": row["category"],
            "availability": row["availability"] in ("True", "true", "1"),
            "price": float(row["price"]),
        }
        resp = requests.post(f"{BASE_URL}/products", json=payload, timeout=10)
        assert resp.status_code == 201, f"Failed to load {payload['name']}"
