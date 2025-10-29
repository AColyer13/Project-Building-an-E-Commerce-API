"""
E-Commerce API - Complete CRUD Application
This application provides a RESTful API for e-commerce operations including:
- User management (customers)
- Product catalog
- Order processing with shopping cart functionality
- Complete database relationships and validation

Database: MySQL with Flask-SQLAlchemy
Validation: Flask-Marshmallow for data serialization
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import ForeignKey, Table, Column, String, Integer, Float, DateTime, select
from marshmallow import ValidationError, fields, validate, validates
from datetime import datetime
from typing import List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)

# DATABASE MODELS

order_product = Table(
    'order_product',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)

class User(Base):
    """
    User Table
    Columns: id, name, address, email (unique), phone, created_at
    Relationships: One-to-Many with Orders
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

class Product(Base):
    """
    Product Table
    Columns: id, product_name, price, description, stock_quantity, category, created_at
    Relationships: Many-to-Many with Orders
    """
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500))
    stock_quantity = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    orders = relationship("Order", secondary=order_product, back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.product_name}', price=${self.price})>"

class Order(Base):
    """
    Order Table
    Columns: id, order_date, user_id (FK), status, total_amount
    Relationships: Many-to-One with User, Many-to-Many with Products
    """
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(20), default="pending")
    total_amount = db.Column(db.Float, default=0.0)
    
    user = relationship("User", back_populates="orders")
    products = relationship("Product", secondary=order_product, back_populates="orders")

    def calculate_total(self):
        """Calculate total amount for this order based on products"""
        total = sum(product.price for product in self.products)
        self.total_amount = total
        return total

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, total=${self.total_amount})>"

# MARSHMALLOW SCHEMAS

class UserSchema(ma.SQLAlchemyAutoSchema):
    """UserSchema - Serialization and validation for User model"""
    class Meta:
        model = User
        load_instance = True
    
    email = fields.Email(required=True, error_messages={'invalid': 'Please enter a valid email address'})
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    address = fields.Str(validate=validate.Length(max=255))
    phone = fields.Str(validate=validate.Length(max=20))
    
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class ProductSchema(ma.SQLAlchemyAutoSchema):
    """ProductSchema - Serialization and validation for Product model"""
    class Meta:
        model = Product
        load_instance = True
    
    product_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    price = fields.Float(required=True, validate=validate.Range(min=0.01))
    description = fields.Str(validate=validate.Length(max=500))
    stock_quantity = fields.Int(validate=validate.Range(min=0))
    category = fields.Str(validate=validate.Length(max=50))
    
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class OrderSchema(ma.SQLAlchemyAutoSchema):
    """OrderSchema - Serialization and validation for Order model"""
    class Meta:
        model = Order
        load_instance = False
        include_fk = True
    
    user_id = fields.Int(required=True)
    status = fields.Str(validate=validate.OneOf(['pending', 'confirmed', 'shipped', 'delivered']))
    
    id = fields.Int(dump_only=True)
    order_date = fields.DateTime(dump_only=True)
    total_amount = fields.Float(dump_only=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# ROOT ENDPOINT

@app.route('/', methods=['GET'])
def home():
    """Root endpoint - API information"""
    return jsonify({
        'message': 'Welcome to E-Commerce API',
        'version': '1.0.0',
        'status': 'running',
        'available_endpoints': {
            'users': {
                'GET /users': 'Get all users',
                'POST /users': 'Create new user',
                'GET /users/<id>': 'Get user by ID',
                'PUT /users/<id>': 'Update user',
                'DELETE /users/<id>': 'Delete user'
            },
            'products': {
                'GET /products': 'Get all products',
                'POST /products': 'Create new product',
                'GET /products/<id>': 'Get product by ID',
                'PUT /products/<id>': 'Update product',
                'DELETE /products/<id>': 'Delete product'
            },
            'orders': {
                'POST /orders': 'Create new order',
                'GET /orders/user/<user_id>': 'Get user orders',
                'GET /orders/<order_id>/products': 'Get order products',
                'PUT /orders/<order_id>/add_product/<product_id>': 'Add product to order',
                'DELETE /orders/<order_id>/remove_product/<product_id>': 'Remove product from order'
            },
            'extras': {
                'PUT /orders/<order_id>/status': 'Update order status',
                'GET /stats': 'Get system statistics'
            }
        },
        'documentation': 'Check README.md for detailed API documentation'
    }), 200

# USER CRUD ENDPOINTS

@app.route('/users', methods=['POST'])
def create_user():
    """POST /users: Create a new user"""
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    existing_user = db.session.execute(select(User).where(User.email == user_data.email)).scalar_one_or_none()
    if existing_user:
        return jsonify({'error': 'A user with this email already exists'}), 409
    
    new_user = user_data
    db.session.add(new_user)
    db.session.commit()

    logger.info(f"User created with ID: {new_user.id}")
    return user_schema.jsonify(new_user), 201

@app.route('/users', methods=['GET'])
def get_users():
    """GET /users: Retrieve all users"""
    query = select(User)
    users = db.session.execute(query).scalars().all()
    
    if not users:
        return jsonify({'message': 'No users found', 'users': []}), 200
    
    return users_schema.jsonify(users), 200

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """GET /users/<id>: Retrieve a user by ID"""
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({'error': f'User with ID {id} not found'}), 404
    
    return user_schema.jsonify(user), 200

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    """PUT /users/<id>: Update a user by ID"""
    user = db.session.get(User, id)

    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    if hasattr(user_data, 'email') and user_data.email != user.email:
        existing_user = db.session.execute(select(User).where(User.email == user_data.email)).scalar_one_or_none()
        if existing_user:
            return jsonify({'error': 'A user with this email already exists'}), 409
    
    user.name = user_data.name
    user.email = user_data.email
    if hasattr(user_data, 'address'):
        user.address = user_data.address
    if hasattr(user_data, 'phone'):
        user.phone = user_data.phone

    db.session.commit()
    return user_schema.jsonify(user), 200

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """DELETE /users/<id>: Delete a user by ID"""
    user = db.session.get(User, id)

    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    
    if user.orders:
        logger.warning(f"User {id} has {len(user.orders)} orders - deletion will cascade")
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted user {id}"}), 200

# PRODUCT CRUD ENDPOINTS

@app.route('/products', methods=['POST'])
def create_product():
    """POST /products: Create a new product"""
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_product = product_data
    db.session.add(new_product)
    db.session.commit()

    logger.info(f"Product created with ID: {new_product.id}")
    return product_schema.jsonify(new_product), 201

@app.route('/products', methods=['GET'])
def get_products():
    """GET /products: Retrieve all products"""
    query = select(Product)
    
    category = request.args.get('category')
    if category:
        query = query.where(Product.category.ilike(f'%{category}%'))
    
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)
    
    products = db.session.execute(query).scalars().all()
    
    if not products:
        return jsonify({'message': 'No products found', 'products': []}), 200
    
    return products_schema.jsonify(products), 200

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    """GET /products/<id>: Retrieve a product by ID"""
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({'error': f'Product with ID {id} not found'}), 404
    
    return product_schema.jsonify(product), 200

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    """PUT /products/<id>: Update a product by ID"""
    product = db.session.get(Product, id)

    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    product.product_name = product_data.product_name
    product.price = product_data.price
    if hasattr(product_data, 'description'):
        product.description = product_data.description
    if hasattr(product_data, 'stock_quantity'):
        product.stock_quantity = product_data.stock_quantity
    if hasattr(product_data, 'category'):
        product.category = product_data.category

    db.session.commit()
    return product_schema.jsonify(product), 200

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    """DELETE /products/<id>: Delete a product by ID"""
    product = db.session.get(Product, id)

    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted product {id}"}), 200

# ORDER CRUD ENDPOINTS

@app.route('/orders', methods=['POST'])
def create_order():
    """POST /orders: Create a new order"""
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    user = db.session.get(User, order_data['user_id'])
    if not user:
        return jsonify({'error': f'User with ID {order_data["user_id"]} not found'}), 404
    
    new_order = Order(
        user_id=order_data['user_id'],
        status=order_data.get('status', 'pending')
    )
    
    db.session.add(new_order)
    db.session.commit()

    logger.info(f"Order created with ID: {new_order.id}")
    return order_schema.jsonify(new_order), 201

@app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['PUT'])
def add_product_to_order(order_id, product_id):
    """PUT /orders/<order_id>/add_product/<product_id>: Add a product to an order"""
    order = db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)

    if not order:
        return jsonify({'error': f'Order with ID {order_id} not found'}), 404
    if not product:
        return jsonify({'error': f'Product with ID {product_id} not found'}), 404
    
    if product in order.products:
        return jsonify({'error': 'Product is already in this order'}), 409
    
    if product.stock_quantity <= 0:
        return jsonify({'error': 'Product is out of stock'}), 400
    
    order.products.append(product)
    product.stock_quantity -= 1
    order.calculate_total()
    
    db.session.commit()
    
    return jsonify({
        'message': f'Product {product.product_name} added to order {order_id}',
        'order_total': order.total_amount
    }), 200

@app.route('/orders/<int:order_id>/remove_product/<int:product_id>', methods=['DELETE'])
def remove_product_from_order(order_id, product_id):
    """DELETE /orders/<order_id>/remove_product/<product_id>: Remove a product from an order"""
    order = db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)

    if not order:
        return jsonify({'error': f'Order with ID {order_id} not found'}), 404
    if not product:
        return jsonify({'error': f'Product with ID {product_id} not found'}), 404
    
    if product not in order.products:
        return jsonify({'error': 'Product is not in this order'}), 404
    
    order.products.remove(product)
    product.stock_quantity += 1
    order.calculate_total()
    
    db.session.commit()
    
    return jsonify({
        'message': f'Product {product.product_name} removed from order {order_id}',
        'order_total': order.total_amount
    }), 200

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    """GET /orders/user/<user_id>: Get all orders for a user"""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': f'User with ID {user_id} not found'}), 404
    
    query = select(Order).where(Order.user_id == user_id)
    orders = db.session.execute(query).scalars().all()
    
    if not orders:
        return jsonify({
            'message': f'No orders found for user {user_id}',
            'orders': []
        }), 200
    
    return orders_schema.jsonify(orders), 200

@app.route('/orders/<int:order_id>/products', methods=['GET'])
def get_order_products(order_id):
    """GET /orders/<order_id>/products: Get all products for an order"""
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({'error': f'Order with ID {order_id} not found'}), 404
    
    if not order.products:
        return jsonify({
            'message': f'No products found in order {order_id}',
            'products': [],
            'order_total': order.total_amount
        }), 200
    
    return jsonify({
        'message': f'Found {len(order.products)} products in order {order_id}',
        'products': products_schema.dump(order.products),
        'order_total': order.total_amount
    }), 200

# EXTRA FEATURES

@app.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status"""
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({'error': f'Order with ID {order_id} not found'}), 404
    
    if not request.json or 'status' not in request.json:
        return jsonify({'error': 'Status is required'}), 400
    
    new_status = request.json['status']
    valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered']
    
    if new_status not in valid_statuses:
        return jsonify({'error': f'Invalid status. Must be one of: {valid_statuses}'}), 400
    
    order.status = new_status
    db.session.commit()
    
    return jsonify({
        'message': f'Order {order_id} status updated to {new_status}',
        'order': order_schema.dump(order)
    }), 200

@app.route('/stats', methods=['GET'])
def get_system_stats():
    """Get system statistics"""
    total_users = len(db.session.execute(select(User)).scalars().all())
    total_products = len(db.session.execute(select(Product)).scalars().all())
    total_orders = len(db.session.execute(select(Order)).scalars().all())
    
    orders = db.session.execute(select(Order)).scalars().all()
    total_revenue = sum(order.total_amount for order in orders)
    
    return jsonify({
        'system_stats': {
            'total_users': total_users,
            'total_products': total_products,
            'total_orders': total_orders,
            'total_revenue': round(total_revenue, 2)
        }
    }), 200

# ERROR HANDLERS

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed for this endpoint'}), 405

# MAIN ENTRY POINT

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        logger.info("Database tables created successfully in MySQL")
        logger.info("Tables created: users, products, orders, order_product")
    
    logger.info("Starting E-Commerce API server")
    logger.info("Users: GET,POST /users | GET,PUT,DELETE /users/<id>")
    logger.info("Products: GET,POST /products | GET,PUT,DELETE /products/<id>")
    logger.info("Orders: POST /orders | GET /orders/user/<id> | GET /orders/<id>/products")
    logger.info("Order Management: PUT /orders/<id>/add_product/<pid> | DELETE /orders/<id>/remove_product/<pid>")
    logger.info("Ready for API testing on http://127.0.0.1:5000")

    app.run(debug=True, host='0.0.0.0', port=5000)