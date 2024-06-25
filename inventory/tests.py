from django.test import TestCase
from .models import Product, Order

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(sku="123", name="Test Product")

    def test_product_stock_initial(self):
        product = Product.objects.get(sku="123")
        self.assertEqual(product.stock, 100)

class OrderTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(sku="123", name="Test Product")

    def test_create_order(self):
        order = Order.objects.create(product=self.product, quantity=5)
        self.product.refresh_from_db
        self.assertEqual(self.product.stock, 95)