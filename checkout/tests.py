from django.test import TestCase
from shop.models import Product
from checkout.models import Order, LineItem
from django.contrib.auth.models import User
from decimal import Decimal

class ProductDeleteTestCase(TestCase):

    def setUp(self):
        """
        Set up a user, product, and order with a line item.
        """
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create a product
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('19.99'),
            description='Test product description',
            in_stock=True
        )

        # Create an order
        self.order = Order.objects.create(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            phone_number='1234567890',
            address_1='123 Test St',
            address_2='Apt 1',
            town='Test Town',
            postcode='12345',
            country='US',
            stripe_pid='stripe_pid_test',
        )

        # Add a line item referencing the product
        self.line_item = LineItem.objects.create(
            order=self.order,
            shop_item=self.product,
            product_name=self.product.name,
            product_price=self.product.price,
            quantity=2,
        )

    def test_delete_product_from_database(self):
        """
        Test deleting a product from the database that exists in an order.
        """
        # Ensure the product and line item are initially created
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(LineItem.objects.count(), 1)
        self.assertEqual(self.line_item.shop_item, self.product)

        # Delete the product from the database
        self.product.delete()

        # Ensure the product is deleted from the database
        self.assertEqual(Product.objects.count(), 0)

        # Ensure that the line item still exists
        self.assertEqual(LineItem.objects.count(), 1)

        # Check if the line item has a null reference to the deleted product
        self.line_item.refresh_from_db()  # Reload the line item from the database
        self.assertIsNone(self.line_item.shop_item)  # The product reference should be None

      

