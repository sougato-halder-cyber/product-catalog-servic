"""Test cases for the Product REST API routes."""
import unittest
from service import app, db
from tests.factories import ProductFactory


class TestProductRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.app_ctx = app.app_context()
        self.app_ctx.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()

    def _create_products(self, count):
        ids = []
        for _ in range(count):
            p = ProductFactory()
            data = p.serialize()
            data.pop("id", None)
            resp = self.client.post("/products", json=data)
            self.assertEqual(resp.status_code, 201)
            ids.append(resp.get_json()["id"])
        return ids

    def test_read_product(self):
        """It should READ a product via API"""
        pid = self._create_products(1)[0]
        resp = self.client.get(f"/products/{pid}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["id"], pid)

    def test_update_product(self):
        """It should UPDATE a product via API"""
        pid = self._create_products(1)[0]
        resp = self.client.put(f"/products/{pid}", json={
            "name": "NewName", "category": "toys",
            "availability": True, "price": 9.99})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "NewName")

    def test_delete_product(self):
        """It should DELETE a product via API"""
        pid = self._create_products(1)[0]
        resp = self.client.delete(f"/products/{pid}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.client.get(f"/products/{pid}").status_code, 404)

    def test_list_all_products(self):
        """It should LIST ALL products"""
        self._create_products(3)
        resp = self.client.get("/products")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.get_json()), 3)

    def test_list_by_name(self):
        """It should LIST products BY NAME"""
        data = {"name": "iPhone", "category": "electronics",
                "availability": True, "price": 999.0}
        self.client.post("/products", json=data)
        resp = self.client.get("/products?name=iPhone")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()[0]["name"], "iPhone")

    def test_list_by_category(self):
        """It should LIST products BY CATEGORY"""
        self.client.post("/products", json={
            "name": "Shirt", "category": "clothing",
            "availability": True, "price": 20.0})
        resp = self.client.get("/products?category=clothing")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()[0]["category"], "clothing")

    def test_list_by_availability(self):
        """It should LIST products BY AVAILABILITY"""
        self.client.post("/products", json={
            "name": "Sofa", "category": "furniture",
            "availability": False, "price": 250.0})
        resp = self.client.get("/products?availability=false")
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.get_json()[0]["availability"])


if __name__ == "__main__":
    unittest.main()
