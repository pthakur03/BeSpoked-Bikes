from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    manufacturer = db.Column(db.String(50), nullable=True)
    style = db.Column(db.String(50), nullable=True)
    purchase_price = db.Column(db.Float, nullable=True)
    sale_price = db.Column(db.Float, nullable=False)
    qty_on_hand = db.Column(db.Integer, nullable=True)
    commission_percentage = db.Column(db.Float, nullable=True)


class Salesperson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    termination_date = db.Column(db.Date)
    manager = db.Column(db.String(50), nullable=True)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    start_date = db.Column(db.Date, nullable=True)


class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    salesperson_id = db.Column(db.Integer, db.ForeignKey('salesperson.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    sales_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    salesperson_commission = db.Column(db.Float, nullable=False)


class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    begin_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    discount_percentage = db.Column(db.Float, nullable=False)


db.create_all()
