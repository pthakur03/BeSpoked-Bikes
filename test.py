import unittest
from datetime import date
from client import *


class TestSalesApp(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        db.init_app(app)
        with app.app_context():
            db.create_all()

        self.client = app.test_client()

        self.salesperson1 = Salesperson(first_name='John')
        self.salesperson2 = Salesperson(first_name='Jane')
        self.product1 = Product(name='Product1', sale_price=10.0)
        self.product2 = Product(name='Product2', sale_price=20.0)
        self.customer1 = Customer(first_name='Customer1')
        self.customer2 = Customer(first_name='Customer2')
        self.discount = Discount(product_id=self.product1.id, begin_date=date.today(), end_date=date.today(), discount_percentage=0.1)

        with app.app_context():
            db.session.add_all([self.salesperson1, self.salesperson2, self.product1, self.product2, self.customer1, self.customer2, self.discount])
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_display_salespersons(self):
        response = self.client.get('/salespersons')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'salespersons': [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]})

    def test_update_salesperson(self):
        response = self.client.put('/salespersons/1', json={'first_name': 'John Smith', 'commission_rate': 0.07})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': 1, 'name': 'John Smith'})

    def test_display_products(self):
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'products': [{'id': 1, 'name': 'Product1', 'sale_price': 10.0}, {'id': 2, 'name': 'Product2', 'sale_price': 20.0}]})

    def test_update_product(self):
        response = self.client.put('/products/1', json={'name': 'Product1', 'price': 8.0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': 1, 'name': 'Product1', 'price': 8.0})

    def test_display_customers(self):
        response = self.client.get('/customers')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'customers': [{'id': 1, 'first_name': 'Customer1'}, {'id': 2, 'first_name': 'Customer2'}]})
