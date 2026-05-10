import os
import logging
from unittest import TestCase
from service.models import Product, Category, db, DataValidationError
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///test.db")

class TestProductModel(TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_read_a_product(self):
        """It should Read a Product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        # Fetch it back
        found_product = Product.find(product.id)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)

    def test_update_a_product(self):
        """It should Update a Product"""
        product = ProductFactory()
        product.create()
        product.description = "testing update"
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.description, "testing update")

    def test_delete_a_product(self):
        """It should Delete a Product"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """It should List all Products in the database"""
        self.assertEqual(len(Product.all()), 0)
        for _ in range(5):
            ProductFactory().create()
        self.assertEqual(len(Product.all()), 5)

    def test_find_by_name(self):
        """It should Find a Product by Name"""
        products = ProductFactory.create_batch(5)
        target_name = products[0].name
        count = len([p for p in products if p.name == target_name])
        found = Product.find_by_name(target_name)
        self.assertEqual(found.count(), count)

    def test_find_by_category(self):
        """It should Find Products by Category"""
        ProductFactory.create_batch(10)
        category = Category.FOOD
        found = Product.find_by_category(category)
        self.assertEqual(found.count(), len([p for p in Product.all() if p.category == category]))

    def test_find_by_availability(self):
            """It should Find Products by Availability"""
            products = ProductFactory.create_batch(10)
            available = products[0].available
            count = len([product for product in products if product.available == available])
            found = Product.find_by_availability(available)
            self.assertEqual(found.count(), count)
            for product in found:
                self.assertEqual(product.available, available)
                
