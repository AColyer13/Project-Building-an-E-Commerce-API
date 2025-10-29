# E-Commerce API

A complete RESTful API built with Flask, SQLAlchemy, and Marshmallow for managing an e-commerce system with users, products, and orders.

## Project Overview

This API provides full CRUD (Create, Read, Update, Delete) operations for:
- Users - Customer management
- Products - Inventory management  
- Orders - Order processing with shopping cart functionality

### Database Relationships
- One-to-Many: One User maps to Many Orders
- Many-to-Many: Orders and Products through an association table

## Technology Stack

- Flask - Web framework
- Flask-SQLAlchemy - Database ORM
- Flask-Marshmallow - Data serialization and validation
- MySQL - Relational database
- Python 3.x - Programming language

## Installation and Setup

### Prerequisites
- Python 3.x installed
- MySQL Server running on port 3306 (default)
- MySQL Workbench (optional, for database visualization)

### Database Setup

1. Open MySQL Workbench
2. Use your existing connection: ecommerce_api
   - Hostname: 127.0.0.1 (localhost)
   - Port: 3306 (default MySQL port)
   - Username: root
   - Password: root

3. Create the database:
   ```sql
   CREATE DATABASE ecommerce_api;
   ```

4. Verify connection: The new ecommerce_api database should appear in the schemas panel.

### Project Setup
```bash
cd ecommerce_api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install Flask Flask-SQLAlchemy Flask-Marshmallow marshmallow-sqlalchemy mysql-connector-python
```

### Configuration

The application uses the following database configuration in index.py:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/ecommerce_api'
```

Configuration details:
- Username: root
- Password: root 
- Host: localhost
- Port: 3306 (default)
- Database: ecommerce_api

### Running the Application
```bash
python index.py
```

Expected output:
```
INFO:__main__:Database tables created successfully in MySQL!
INFO:__main__:Tables created: users, products, orders, order_product
INFO:__main__:Starting E-Commerce API server...
INFO:__main__:Ready for API testing
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

The API will be accessible at http://localhost:5000

## Database Schema

### Users Table
| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| name | String(100) | Not Null |
| address | String(255) | Optional |
| email | String(100) | Unique, Not Null |
| phone | String(20) | Optional |
| created_at | DateTime | Auto-generated |

### Products Table
| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| product_name | String(100) | Not Null |
| price | Float | Not Null |
| description | String(500) | Optional |
| stock_quantity | Integer | Default: 0 |
| category | String(50) | Optional |
| created_at | DateTime | Auto-generated |

### Orders Table
| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| order_date | DateTime | Auto-generated |
| user_id | Integer | Foreign Key → Users.id |
| status | String(20) | Default: 'pending' |
| total_amount | Float | Calculated field |

### Order_Product Association Table
| Field | Constraints |
|-------|-------------|
| order_id | Foreign Key → Orders.id |
| product_id | Foreign Key → Products.id |

## API Endpoints

### User Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users` | Create a new user |
| GET | `/users` | Get all users |
| GET | `/users/<id>` | Get user by ID |
| PUT | `/users/<id>` | Update user by ID |
| DELETE | `/users/<id>` | Delete user by ID |

### Product Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/products` | Create a new product |
| GET | `/products` | Get all products |
| GET | `/products/<id>` | Get product by ID |
| PUT | `/products/<id>` | Update product by ID |
| DELETE | `/products/<id>` | Delete product by ID |

### Order Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/orders` | Create a new order |
| PUT | `/orders/<order_id>/add_product/<product_id>` | Add product to order |
| DELETE | `/orders/<order_id>/remove_product/<product_id>` | Remove product from order |
| GET | `/orders/user/<user_id>` | Get all orders for a user |
| GET | `/orders/<order_id>/products` | Get all products in an order |

### Additional Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/orders/<order_id>/status` | Update order status |
| GET | `/stats` | Get system statistics |

## Testing

### Interactive API Client

The project includes api_client.py for testing all API endpoints interactively.

#### Running the Client

```bash
# Terminal 1: Run the Flask API
python index.py

# Terminal 2: Run the API Client
python api_client.py
```

#### Available Operations

User Operations:
- Create User
- Get All Users 
- Get User by ID
- Update User
- Delete User

Product Operations:
- Create Product
- Get All Products
- Get Product by ID 
- Update Product
- Delete Product

Order Operations:
- Create Order (with product selection)
- Get User Orders
- Get Order Products
- Add Product to Order
- Remove Product from Order

Additional Operations:
- Update Order Status
- Get System Statistics
- Run Complete Test Suite

#### Create Order Workflow

When creating an order, the client displays:
- All available products in a formatted table
- Product details (ID, name, price, stock, category)
- Option to select multiple products
- Real-time feedback on product additions

Example:
```
Creating New Order
Enter User ID for the order: 1

Available Products:
ID    Name                 Price      Stock    Category       
1     Laptop               $999.99    10       Electronics    
2     Mouse                $29.99     50       Electronics    
3     Coffee Mug           $12.99     100      Home          

Select Products for Order:
Enter product IDs separated by commas (e.g., 1,3,5) or 'none' for empty order:
Product IDs: 1,2

Order 1 created successfully!
Adding 2 products to order...
  Product Laptop added to order 1
  Product Mouse added to order 2
```

#### Automated Test Suite

Run the complete test suite to verify all functionality:
- Creates sample users
- Creates sample products  
- Creates sample orders
- Adds products to orders
- Updates order status
- Generates system statistics
- Displays formatted results

---

### Postman Testing

#### Setup

1. Open Postman
2. Create a new collection: "E-Commerce API"
3. Set base URL: http://localhost:5000

#### Sample Requests

Create a User:
```http
POST /users
Content-Type: application/json

{
  "name": "James Dean",
  "email": "jd@gmail.com",
  "address": "545 Elm Street",
  "phone": "123-4567"
}
```

Create a Product:
```http
POST /products
Content-Type: application/json

{
  "product_name": "Monitor",
  "price": 99.99,
  "description": "4k Monitor",
  "stock_quantity": 20,
  "category": "Electronics"
}
```

Create an Order:
```http
POST /orders
Content-Type: application/json

{
  "user_id": 1
}
```

Add Product to Order:
```http
PUT /orders/1/add_product/1
```

Get Order Products:
```http
GET /orders/1/products
```

#### Testing Workflow

1. Create test users with varying details
2. Create products across different categories
3. Create orders for different users
4. Test product additions to orders
5. Test filtering with query parameters
6. Test updates and deletions
7. Test error handling with invalid data

## API Response Examples

### User Creation Response
```json
{
  "id": 1,
  "name": "Jane Doe",
  "email": "jane@msn.com",
  "address": "545 Elm Street",
  "phone": "123-4567",
  "created_at": "2024-01-15T10:30:00"
}
```

### Product List with Filtering
```http
GET /products?category=Electronics&min_price=50&max_price=200
```

```json
{
  "message": "Found 3 products",
  "products": [
    {
      "id": 1,
      "product_name": "Monitor",
      "price": 99.99,
      "category": "Electronics",
      "stock_quantity": 20
    }
  ]
}
```

### Order with Products
```json
{
  "message": "Found 2 products in order 1",
  "products": [
    {
      "id": 1,
      "product_name": "Monitor",
      "price": 99.99
    },
    {
      "id": 2,
      "product_name": "Phone Case",
      "price": 19.99
    }
  ],
  "order_total": 119.98
}
```

## Error Handling

### Validation Errors (400)
```json
{
  "errors": {
    "email": ["Please enter a valid email address"],
    "price": ["Price must be greater than $0.00"]
  }
}
```

### Not Found Errors (404)
```json
{
  "error": "User with ID 999 not found"
}
```

### Conflict Errors (409)
```json
{
  "error": "A user with this email already exists"
}
```

## Data Validation

- Email validation for proper format
- Price validation for positive values
- Stock management to prevent overselling
- Duplicate prevention for order items
- Foreign key validation for referential integrity

## Business Logic Features

- Automatic order total calculation
- Stock quantity management
- Order status tracking (pending, confirmed, shipped, delivered)
- Cascade deletion for user and related orders
- Comprehensive logging for debugging

## Database Verification

After running the Flask application, verify table creation in MySQL Workbench:

### Verify Tables
```sql
USE ecommerce_api;
SHOW TABLES;
```

### View Table Structures
```sql
DESCRIBE users;
DESCRIBE products;
DESCRIBE orders;
DESCRIBE order_product;
```

### Check Data
```sql
SELECT * FROM users;
SELECT * FROM products;
SELECT * FROM orders;
```

### View Orders with Customer Information
```sql
SELECT 
    o.id as order_id,
    o.order_date,
    o.status,
    o.total_amount,
    u.name as customer_name,
    u.email
FROM orders o 
JOIN users u ON o.user_id = u.id;
```

### View Products in Orders
```sql
SELECT 
    o.id as order_id,
    u.name as customer,
    p.product_name,
    p.price
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN order_product op ON o.id = op.order_id
JOIN products p ON op.product_id = p.id
ORDER BY o.id;
```

### System Metrics
```sql
SELECT 
    'Total Users' as metric, COUNT(*) as count FROM users
UNION ALL
SELECT 
    'Total Products' as metric, COUNT(*) as count FROM products
UNION ALL
SELECT 
    'Total Orders' as metric, COUNT(*) as count FROM orders
UNION ALL
SELECT 
    'Total Order-Product Links' as metric, COUNT(*) as count FROM order_product;
```

### Real-Time Monitoring

Keep MySQL Workbench open during testing:
1. Right-click the ecommerce_api schema
2. Select "Refresh All"
3. Run queries to verify data changes

## Project Structure

```
ecommerce_api/
├── index.py          # Main Flask API application
├── api_client.py     # Interactive CLI client for testing
├── README.md         # Project documentation
├── venv/             # Virtual environment
└── requirements.txt  # Dependencies (optional)
```

### File Descriptions

| File | Purpose |
|------|---------|
| index.py | Flask REST API server with all endpoints and database models |
| api_client.py | Interactive command-line client for API testing |
| README.md | Project documentation |

## Quick Start

### Start Services

Terminal 1:
```bash
python index.py
```

Terminal 2:
```bash
python api_client.py
```

### Recommended Testing Order

1. Run automated test suite (option 18)
2. Perform manual testing with menu options
3. Verify data in MySQL Workbench
4. Test edge cases with Postman

### Common Workflows

Create and View an Order:
```
1. Create a product (option 6)
2. Create a user (option 1)
3. Create an order (option 11)
4. View order contents (option 13)
```

Run Complete Test:
```
1. Select option 18
2. Confirm execution
3. Review results
```



## Future Enhancements

- Add user authentication with JWT tokens
- Implement pagination for large datasets
- Add search functionality
- Create admin endpoints
- Add order history tracking
- Implement email notifications
- Add product image support
- Persist shopping cart data
- Generate order receipts and invoices
- Add advanced filtering capabilities

## Connection Verification

```python
import mysql.connector

try:
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        database='ecommerce_api'
    )
    print("MySQL connection successful")
    connection.close()

except Exception as e:
    print(f"Connection failed: {e}")
```

---

*This project demonstrates Flask, SQLAlchemy, database relationship design, and RESTful API development principles.*
