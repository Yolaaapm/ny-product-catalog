import os
import logging
from unittest import TestCase
from service import app
from service.models import db, Product, init_db
from service.common import status
from tests.factories import ProductFactory

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///test.db")
BASE_URL = "/products"

class TestProductRoutes(TestCase):
    """Product Service Rest Api Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    def setUp(self):
        """Runs before each test"""
        db.session.query(Product).delete()
        db.session.commit()
        self.client = app.test_client()

    def _create_products(self, count):
        """Helper method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            products.append(test_product)
        return products

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_get_product(self):
        """It should Get a single Product"""
        test_product = self._create_products(1)[0]
        # Ambil produk yang baru dibuat (asumsi ID mulai dari 1 di db bersih)
        response = self.client.get(f"{BASE_URL}/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product(self):
        """It should Update an existing Product"""
        test_product = ProductFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        new_product = response.get_json()
        new_product["description"] = "updated description"
        response = self.client.put(f"{BASE_URL}/{new_product['id']}", json=new_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["description"], "updated description")

    def test_delete_product(self):
        """It should Delete a Product"""
        test_product = self._create_products(1)[0]
        response = self.client.delete(f"{BASE_URL}/1")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_product_list(self):
        """It should Get a list of Products"""
        self._create_products(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.get_json()), 5)

    def test_query_by_name(self):
        """It should Query Products by Name"""
        products = self._create_products(5)
        test_name = products[0].name
        response = self.client.get(BASE_URL, query_string=f"name={test_name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_query_by_category(self):
        """It should Query Products by Category"""
        products = self._create_products(10)
        test_category = products[0].category
        response = self.client.get(BASE_URL, query_string=f"category={test_category.name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_query_by_availability(self):
        """It should Query Products by Availability"""
        self._create_products(10)
        response = self.client.get(BASE_URL, query_string="available=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
