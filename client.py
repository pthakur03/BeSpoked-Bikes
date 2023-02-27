from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from app import db, Salesperson, Product, Customer, Sales, Discount

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bespoked.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# Standard CRUD ops for salespersons, products, & customers (Delete not necessary?)

@app.route('/customers', methods=['GET'])
def get_salespersons():
    salespersons = Salesperson.query.all()
    return jsonify([salesperson.serialize() for salesperson in salespersons])


@app.route('/salespersons/<int:salesperson_id>', methods=['GET'])
def get_salesperson(salesperson_id):
    salesperson = Salesperson.query.get_or_404(salesperson_id)
    return jsonify(salesperson.serialize())


@app.route('/salespersons', methods=['POST'])
def create_salesperson():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    if not first_name or not last_name:
        return jsonify({'error': 'First name and last name are required'}), 400
    salesperson = Salesperson.query.filter_by(first_name=first_name, last_name=last_name).first()
    if salesperson:
        return jsonify({'error': 'Salesperson already exists'}), 409
    salesperson = Salesperson(**data)
    db.session.add(salesperson)
    db.session.commit()
    return jsonify(salesperson.serialize())


@app.route('/salespersons/<int:salesperson_id>', methods=['PUT'])
def update_salesperson(salesperson_id):
    data = request.get_json()
    salesperson = Salesperson.query.get_or_404(salesperson_id)
    for key, value in data.items():
        setattr(salesperson, key, value)
    db.session.commit()
    return jsonify(salesperson.serialize())


@app.route('/salespersons/<int:salesperson_id>', methods=['DELETE'])
def delete_salesperson(salesperson_id):
    salesperson = Salesperson.query.get_or_404(salesperson_id)
    db.session.delete(salesperson)
    db.session.commit()
    return '', 204


@app.route('/customers', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])


@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.serialize())


@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Product name is required'}), 400
    product = Product.query.filter_by(name=name).first()
    if product:
        return jsonify({'error': 'Product already exists'}), 409
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.serialize())


def update_product(product_id, new_name=None, new_price=None):
    product = Product.query.get_or_404(product_id)
    discount = Discount.query.filter_by(product_id=product_id).first()
    if discount and discount.begin_date <= datetime.now().date() <= discount.end_date:
        new_price = product.price * (1 - discount.discount_percentage/100)
    if new_name:
        product.name = new_name
    if new_price:
        product.price = new_price
    data = request.get_json()
    for key, value in data.items():
        setattr(product, key, value)
    db.session.commit()
    return jsonify(product.serialize())


@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.serialize() for customer in customers])


@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.serialize())


@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    customer = Customer(**data)
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.serialize())


@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    customer = Customer.query.get_or_404(customer_id)
    for key, value in data.items():
        setattr(customer, key, value)
    db.session.commit()
    return jsonify(customer.serialize())


@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return '', 204


@app.route('/sales', methods=['GET'])
def get_sales():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    query = db.session.query(
        Sales,
        Product.name.label('product_name'),
        Customer.first_name.label('customer_first_name'),
        Customer.last_name.label('customer_last_name'),
        Salesperson.first_name.label('salesperson_first_name'),
        Salesperson.last_name.label('salesperson_last_name')
    ).join(Product).join(Customer).join(Salesperson)
    if start_date:
        query = query.filter(Sales.sales_date >= start_date)
    if end_date:
        query = query.filter(Sales.sales_date <= end_date)
    sales = []
    for sale, product_name, customer_first_name, customer_last_name, salesperson_first_name, salesperson_last_name in query.all():
        sales.append({
            'id': sale.id,
            'product_name': product_name,
            'customer_first_name': customer_first_name,
            'customer_last_name': customer_last_name,
            'salesperson_first_name': salesperson_first_name,
            'salesperson_last_name': salesperson_last_name,
            'sales_date': sale.sales_date.isoformat(),
            'price': sale.price,
            'salesperson_commission': sale.salesperson_commission
        })
    return jsonify(sales)


@app.route('/sales', methods=['POST'])
def create_sale():
    data = request.get_json()
    product_id = data.get('product_id')
    salesperson_id = data.get('salesperson_id')
    customer_id = data.get('customer_id')
    sales_date = data.get('sales_date')
    quantity = data.get('quantity')
    product = Product.query.get_or_404(product_id)
    salesperson = Salesperson.query.get_or_404(salesperson_id)
    customer = Customer.query.get_or_404(customer_id)
    price = product.sale_price * quantity
    salesperson_commission = price * salesperson.commission_percentage / 100
    sale = Sales(
        product_id=product_id,
        salesperson_id=salesperson_id,
        customer_id=customer_id,
        sales_date=sales_date,
        quantity=quantity,
        price=price,
        salesperson_commission=salesperson_commission
    )
    db.session.add(sale)
    db.session.commit()
    return jsonify(sale.serialize())


def get_salesperson_commission(salesperson_id, quarter=None):
    if quarter is None:
        now = datetime.now()
        quarter = (now.month - 1) // 3 + 1

    start_date = datetime(now.year, 3 * quarter - 2, 1)
    end_date = datetime(now.year, 3 * quarter, 1) - timedelta(days=1)

    sales = db.session.query(Sales).filter_by(salesperson_id=salesperson_id).filter(Sales.sales_date >= start_date,
                                                                                    Sales.sales_date <= end_date).all()

    commission_total = 0
    for sale in sales:
        commission_total += sale.salesperson_commission
    return commission_total


@app.route('/salespersons/<int:salesperson_id>/commissions', methods=['GET'])
def get_salesperson_commissions(salesperson_id):
    commissions = {}
    for quarter in range(1, 5):
        commission_total = get_salesperson_commission(salesperson_id, quarter=quarter)
        commissions[f'Q{quarter}'] = commission_total
    return jsonify(commissions)
