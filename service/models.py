"""Test cases for the Product model."""
import unittest
from service import app, db
from service.models import Product
from tests.factories import ProductFactory


class TestProductModel(unittest.TestCase):
    def setUp(self):
        self.app_ctx = app.app_context()
        self.app_ctx.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()

    def _create_product(self):
        product = ProductFactory()
        product.id = None
        product.create()
        return product

    def test_read_a_product(self):
        """It should READ a Product"""
        product = self._create_product()
        found = Product.find(product.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.name, product.name)

    def test_update_a_product(self):
        """It should UPDATE a Product"""
        product = self._create_product()
        product.name = "Updated Name"
        product.update()
        self.assertEqual(Product.find(product.id).name, "Updated Name")

    def test_delete_a_product(self):
        """It should DELETE a Product"""
        product = self._create_product()
        product.delete()
        self.assertIsNone(Product.find(product.id))

    def test_list_all_products(self):
        """It should LIST ALL Products"""
        for _ in range(5):
            self._create_product()
        self.assertEqual(len(Product.all()), 5)

    def test_find_by_name(self):
        """It should FIND Products BY NAME"""
        product = self._create_product()
        product.name = "Laptop"
        product.update()
        results = Product.find_by_name("Laptop")
        self.assertGreaterEqual(len(results), 1)

    def test_find_by_category(self):
        """It should FIND Products BY CATEGORY"""
        product = self._create_product()
        product.category = "electronics"
        product.update()
        results = Product.find_by_category("electronics")
        self.assertGreaterEqual(len(results), 1)

    def test_find_by_availability(self):
        """It should FIND Products BY AVAILABILITY"""
        product = self._create_product()
        product.availability = True
        product.update()
        results = Product.find_by_availability(True)
        self.assertGreaterEqual(len(results), 1)


if __name__ == "__main__":
    unittest.main()
