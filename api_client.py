"""
E-Commerce API Client - Interactive Command Line Interface
This script provides a command-line interface to interact with
the e-commerce API. It allows testing all endpoints with sample data
or custom input.

Run this while the Flask API is running on localhost:5000
"""

import requests
import json
from datetime import datetime
import sys

BASE_URL = "http://localhost:5000"
HEADERS = {"Content-Type": "application/json"}

class APIClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS
        self.session = requests.Session()
        
    def make_request(self, method, endpoint, data=None, params=None):
        """Make HTTP request to API and handle response"""
        url = f"{self.base_url}{endpoint}"
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=self.headers)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, headers=self.headers)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url)
            else:
                print(f"Error: Unsupported method: {method}")
                return None
                
            return self.handle_response(response)
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to API. Make sure Flask app is running on localhost:5000")
            return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None
    
    def handle_response(self, response):
        """Handle API response and display formatted output"""
        print(f"\nStatus Code: {response.status_code}")
        
        try:
            data = response.json()
            if response.status_code in [200, 201]:
                print("Success")
                print(f"Response: {json.dumps(data, indent=2)}")
            else:
                print("Error Response:")
                print(f"Details: {json.dumps(data, indent=2)}")
            return data
        except json.JSONDecodeError:
            print(f"Response: {response.text}")
            return response.text

    # USER ENDPOINTS
    
    def create_user(self):
        """POST /users - Create new user"""
        print("\nCreating New User")
        print("-" * 40)
        
        while True:
            name = input("Enter name (required): ").strip()
            if name:
                break
            print("Required field!")
        
        while True:
            email = input("Enter email (required): ").strip()
            if email and '@' in email:
                break
            print("Required field!")
        
        while True:
            address = input("Enter address (required): ").strip()
            if address:
                break
            print("Required field!")
        
        while True:
            phone = input("Enter phone (required): ").strip()
            if phone:
                break
            print("Required field!")
        
        data = {
            "name": name,
            "email": email,
            "address": address,
            "phone": phone
        }
        
        print(f"Creating user with data: {json.dumps(data, indent=2)}")
        return self.make_request('POST', '/users', data)
    
    def get_all_users(self):
        """GET /users - Get all users"""
        print("\nGetting All Users")
        print("-" * 40)
        return self.make_request('GET', '/users')
    
    def get_user_by_id(self):
        """GET /users/<id> - Get user by ID"""
        print("\nGetting User by ID")
        print("-" * 40)
        user_id = input("Enter User ID: ").strip()
        if not user_id.isdigit():
            print("Invalid User ID")
            return None
        return self.make_request('GET', f'/users/{user_id}')
    
    def update_user(self):
        """PUT /users/<id> - Update user"""
        print("\nUpdating User")
        print("-" * 40)
        user_id = input("Enter User ID to update: ").strip()
        if not user_id.isdigit():
            print("Invalid User ID")
            return None
            
        name = input("Enter new name: ").strip()
        email = input("Enter new email: ").strip()
        address = input("Enter new address (optional): ").strip()
        phone = input("Enter new phone (optional): ").strip()
        
        data = {"name": name, "email": email}
        if address:
            data["address"] = address
        if phone:
            data["phone"] = phone
            
        return self.make_request('PUT', f'/users/{user_id}', data)
    
    def delete_user(self):
        """DELETE /users/<id> - Delete user"""
        print("\nDeleting User")
        print("-" * 40)
        user_id = input("Enter User ID to delete: ").strip()
        if not user_id.isdigit():
            print("Invalid User ID")
            return None
            
        confirm = input(f"Are you sure you want to delete user {user_id}? (y/N): ").strip().lower()
        if confirm == 'y':
            return self.make_request('DELETE', f'/users/{user_id}')
        else:
            print("Deletion cancelled")
            return None

    # PRODUCT ENDPOINTS
    
    def create_product(self):
        """POST /products - Create new product"""
        print("\nCreating New Product")
        print("-" * 40)
        
        while True:
            name = input("Enter product name (required): ").strip()
            if name:
                break
            print("Required field!")
        
        while True:
            price_input = input("Enter price (required): ").strip()
            try:
                price = float(price_input)
                if price > 0:
                    break
                else:
                    print("Required field!")
            except ValueError:
                print("Required field!")
        
        while True:
            description = input("Enter description (required): ").strip()
            if description:
                break
            print("Required field!")
        
        while True:
            stock_input = input("Enter stock quantity (required): ").strip()
            try:
                stock = int(stock_input)
                if stock >= 0:
                    break
                else:
                    print("Required field!")
            except ValueError:
                print("Required field!")
        
        while True:
            category = input("Enter category (required): ").strip()
            if category:
                break
            print("Required field!")
        
        data = {
            "product_name": name,
            "price": price,
            "description": description,
            "stock_quantity": stock,
            "category": category
        }
        
        print(f"Creating product with data: {json.dumps(data, indent=2)}")
        return self.make_request('POST', '/products', data)
    
    def get_all_products(self):
        """GET /products - Get all products"""
        print("\nGetting All Products")
        print("-" * 40)
        
        use_filters = input("Use filters? (y/N): ").strip().lower() == 'y'
        params = {}
        
        if use_filters:
            category = input("Filter by category (optional): ").strip()
            min_price = input("Minimum price (optional): ").strip()
            max_price = input("Maximum price (optional): ").strip()
            
            if category:
                params['category'] = category
            if min_price and min_price.replace('.', '').isdigit():
                params['min_price'] = float(min_price)
            if max_price and max_price.replace('.', '').isdigit():
                params['max_price'] = float(max_price)
        
        return self.make_request('GET', '/products', params=params)
    
    def get_product_by_id(self):
        """GET /products/<id> - Get product by ID"""
        print("\nGetting Product by ID")
        print("-" * 40)
        product_id = input("Enter Product ID: ").strip()
        if not product_id.isdigit():
            print("Invalid Product ID")
            return None
        return self.make_request('GET', f'/products/{product_id}')
    
    def update_product(self):
        """PUT /products/<id> - Update product"""
        print("\nUpdating Product")
        print("-" * 40)
        product_id = input("Enter Product ID to update: ").strip()
        if not product_id.isdigit():
            print("Invalid Product ID")
            return None
            
        name = input("Enter new product name: ").strip()
        price = input("Enter new price: ").strip()
        description = input("Enter new description (optional): ").strip()
        stock = input("Enter new stock quantity (optional): ").strip()
        category = input("Enter new category (optional): ").strip()
        
        try:
            data = {
                "product_name": name,
                "price": float(price)
            }
            if description:
                data["description"] = description
            if stock and stock.isdigit():
                data["stock_quantity"] = int(stock)
            if category:
                data["category"] = category
        except ValueError:
            print("Invalid price format")
            return None
            
        return self.make_request('PUT', f'/products/{product_id}', data)
    
    def delete_product(self):
        """DELETE /products/<id> - Delete product"""
        print("\nDeleting Product")
        print("-" * 40)
        product_id = input("Enter Product ID to delete: ").strip()
        if not product_id.isdigit():
            print("Invalid Product ID")
            return None
            
        confirm = input(f"Are you sure you want to delete product {product_id}? (y/N): ").strip().lower()
        if confirm == 'y':
            return self.make_request('DELETE', f'/products/{product_id}')
        else:
            print("Deletion cancelled")
            return None

    # ORDER ENDPOINTS
    
    def create_order(self):
        """POST /orders - Create new order with products"""
        print("\nCreating New Order")
        print("-" * 40)
        
        user_id = input("Enter User ID for the order: ").strip()
        if not user_id.isdigit():
            print("Invalid User ID")
            return None
        
        print("\nAvailable Products:")
        print("-" * 70)
        products_response = self.make_request('GET', '/products')
        
        if not products_response or not isinstance(products_response, list) or len(products_response) == 0:
            print("No products available. Create some products first!")
            return None
        
        print(f"{'ID':<5} {'Name':<20} {'Price':<10} {'Stock':<8} {'Category':<15}")
        print("-" * 70)
        for product in products_response:
            print(f"{product['id']:<5} {product['product_name'][:19]:<20} ${product['price']:<9.2f} {product.get('stock_quantity', 0):<8} {product.get('category', 'N/A')[:14]:<15}")
        
        print("\nSelect Products for Order:")
        print("Enter product IDs separated by commas (e.g., 1,3,5) or 'none' for empty order:")
        
        product_selection = input("Product IDs: ").strip().lower()
        
        selected_product_ids = []
        if product_selection != 'none' and product_selection:
            try:
                id_strings = [id_str.strip() for id_str in product_selection.split(',')]
                selected_product_ids = [int(id_str) for id_str in id_strings if id_str.isdigit()]
                
                if not selected_product_ids:
                    print("No valid product IDs entered")
                    return None
                
                available_ids = [p['id'] for p in products_response]
                invalid_ids = [pid for pid in selected_product_ids if pid not in available_ids]
                
                if invalid_ids:
                    print(f"Invalid product IDs: {invalid_ids}")
                    return None
                    
            except ValueError:
                print("Invalid format. Use numbers separated by commas.")
                return None
        
        print(f"\nCreating order for user {user_id}...")
        order_data = {"user_id": int(user_id)}
        order_response = self.make_request('POST', '/orders', order_data)
        
        if not order_response or 'id' not in order_response:
            print("Failed to create order")
            return None
            
        order_id = order_response['id']
        print(f"Order {order_id} created successfully!")
        
        if selected_product_ids:
            print(f"\nAdding {len(selected_product_ids)} products to order...")
            successful_adds = 0
            
            for product_id in selected_product_ids:
                print(f"  Adding product {product_id}...")
                add_response = self.make_request('PUT', f'/orders/{order_id}/add_product/{product_id}')
                
                if add_response and isinstance(add_response, dict) and 'message' in add_response:
                    print(f"  {add_response['message']}")
                    successful_adds += 1
                else:
                    print(f"  Failed to add product {product_id}")
            
            print(f"\nSuccessfully added {successful_adds}/{len(selected_product_ids)} products to order!")
            
            print(f"\nFinal Order Summary:")
            final_order = self.make_request('GET', f'/orders/{order_id}/products')
            
        else:
            print("\nEmpty order created. You can add products later using 'Add Product to Order'.")
            
        return order_response
    
    def get_user_orders(self):
        """GET /orders/user/<user_id> - Get user orders"""
        print("\nGetting User Orders")
        print("-" * 40)
        user_id = input("Enter User ID: ").strip()
        if not user_id.isdigit():
            print("Invalid User ID")
            return None
        return self.make_request('GET', f'/orders/user/{user_id}')
    
    def get_order_products(self):
        """GET /orders/<order_id>/products - Get order products"""
        print("\nGetting Order Products")
        print("-" * 40)
        order_id = input("Enter Order ID: ").strip()
        if not order_id.isdigit():
            print("Invalid Order ID")
            return None
        return self.make_request('GET', f'/orders/{order_id}/products')
    
    def add_product_to_order(self):
        """PUT /orders/<order_id>/add_product/<product_id> - Add product to order"""
        print("\nAdding Product to Order")
        print("-" * 40)
        order_id = input("Enter Order ID: ").strip()
        product_id = input("Enter Product ID to add: ").strip()
        
        if not order_id.isdigit() or not product_id.isdigit():
            print("Invalid Order ID or Product ID")
            return None
            
        return self.make_request('PUT', f'/orders/{order_id}/add_product/{product_id}')
    
    def remove_product_from_order(self):
        """DELETE /orders/<order_id>/remove_product/<product_id> - Remove product from order"""
        print("\nRemoving Product from Order")
        print("-" * 40)
        order_id = input("Enter Order ID: ").strip()
        product_id = input("Enter Product ID to remove: ").strip()
        
        if not order_id.isdigit() or not product_id.isdigit():
            print("Invalid Order ID or Product ID")
            return None
            
        return self.make_request('DELETE', f'/orders/{order_id}/remove_product/{product_id}')

    # EXTRA ENDPOINTS
    
    def update_order_status(self):
        """PUT /orders/<order_id>/status - Update order status"""
        print("\nUpdating Order Status")
        print("-" * 40)
        order_id = input("Enter Order ID: ").strip()
        if not order_id.isdigit():
            print("Invalid Order ID")
            return None
            
        print("Available statuses: pending, confirmed, shipped, delivered")
        status = input("Enter new status: ").strip().lower()
        
        valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered']
        if status not in valid_statuses:
            print(f"Invalid status. Must be one of: {valid_statuses}")
            return None
            
        data = {"status": status}
        return self.make_request('PUT', f'/orders/{order_id}/status', data)
    
    def get_system_stats(self):
        """GET /stats - Get system statistics"""
        print("\nGetting System Statistics")
        print("-" * 40)
        return self.make_request('GET', '/stats')

    # AUTOMATED TESTING
    
    def run_complete_test_suite(self):
        """Run a complete test of all endpoints with sample data"""
        print("\nRunning Complete Test Suite")
        print("=" * 60)
        
        print("\n1. Creating sample users...")
        user_ids = []
        sample_users = [
            {
                "name": "Test User 1",
                "email": f"testuser1_{datetime.now().strftime('%H%M%S')}@email.com",
                "address": "123 Test Street, Test City, TS 12345",
                "phone": "555-0001"
            },
            {
                "name": "Test User 2", 
                "email": f"testuser2_{datetime.now().strftime('%H%M%S')}@email.com",
                "address": "456 Sample Ave, Sample City, SC 67890",
                "phone": "555-0002"
            }
        ]
        
        for user_data in sample_users:
            print(f"Creating user: {user_data['name']}")
            response = self.make_request('POST', '/users', user_data)
            if response and 'id' in response:
                user_ids.append(response['id'])
        
        print("\n2. Creating sample products...")
        product_ids = []
        sample_products = [
            {
                "product_name": "Test Laptop",
                "price": 999.99,
                "description": "High-performance test laptop",
                "stock_quantity": 10,
                "category": "Electronics"
            },
            {
                "product_name": "Test Mouse",
                "price": 29.99,
                "description": "Wireless test mouse",
                "stock_quantity": 50,
                "category": "Electronics"
            },
            {
                "product_name": "Test Coffee Mug",
                "price": 12.99,
                "description": "Ceramic test mug",
                "stock_quantity": 100,
                "category": "Home"
            }
        ]
        
        for product_data in sample_products:
            print(f"Creating product: {product_data['product_name']}")
            response = self.make_request('POST', '/products', product_data)
            if response and 'id' in response:
                product_ids.append(response['id'])
        
        print("\n3. Getting all users...")
        self.get_all_users()
        
        print("\n4. Getting all products...")
        self.get_all_products()
        
        print("\n5. Creating orders...")
        order_ids = []
        for user_id in user_ids:
            data = {"user_id": user_id}
            response = self.make_request('POST', '/orders', data)
            if response and 'id' in response:
                order_ids.append(response['id'])
        
        print("\n6. Adding products to orders...")
        if order_ids and product_ids:
            for i, order_id in enumerate(order_ids):
                for j in range(min(2, len(product_ids))):
                    product_id = product_ids[j]
                    self.make_request('PUT', f'/orders/{order_id}/add_product/{product_id}')
        
        print("\n7. Getting order details...")
        for order_id in order_ids:
            self.make_request('GET', f'/orders/{order_id}/products')
        
        print("\n8. Updating order statuses...")
        if order_ids:
            data = {"status": "confirmed"}
            self.make_request('PUT', f'/orders/{order_ids[0]}/status', data)
        
        print("\n9. Getting system statistics...")
        self.get_system_stats()
        
        print("\nComplete test suite finished!")


def display_main_menu():
    """Display the main menu"""
    print("\n" + "=" * 60)
    print("E-COMMERCE API CLIENT")
    print("=" * 60)
    print("USER OPERATIONS:")
    print("  1.  Create User")
    print("  2.  Get All Users") 
    print("  3.  Get User by ID")
    print("  4.  Update User")
    print("  5.  Delete User")
    print("\nPRODUCT OPERATIONS:")
    print("  6.  Create Product")
    print("  7.  Get All Products")
    print("  8.  Get Product by ID") 
    print("  9.  Update Product")
    print("  10. Delete Product")
    print("\nORDER OPERATIONS:")
    print("  11. Create Order")
    print("  12. Get User Orders")
    print("  13. Get Order Products")
    print("  14. Add Product to Order")
    print("  15. Remove Product from Order")
    print("\nEXTRA OPERATIONS:")
    print("  16. Update Order Status")
    print("  17. Get System Statistics")
    print("\nAUTOMATED TESTING:")
    print("  18. Run Complete Test Suite")
    print("\n  0.  Exit")
    print("-" * 60)


def main():
    """Main application loop"""
    client = APIClient()
    
    print("Starting E-Commerce API Client...")
    print("Make sure your Flask API is running on http://localhost:5000")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("Connected to API successfully!")
        else:
            print("API connection established but got unexpected response")
    except:
        print("Could not connect to API. Make sure Flask app is running!")
        print("Press Enter to continue anyway...")
        input()
    
    while True:
        display_main_menu()
        choice = input("Enter your choice (0-18): ").strip()
        
        try:
            if choice == '0':
                print("Goodbye!")
                break
            elif choice == '1':
                client.create_user()
            elif choice == '2':
                client.get_all_users()
            elif choice == '3':
                client.get_user_by_id()
            elif choice == '4':
                client.update_user()
            elif choice == '5':
                client.delete_user()
            elif choice == '6':
                client.create_product()
            elif choice == '7':
                client.get_all_products()
            elif choice == '8':
                client.get_product_by_id()
            elif choice == '9':
                client.update_product()
            elif choice == '10':
                client.delete_product()
            elif choice == '11':
                client.create_order()
            elif choice == '12':
                client.get_user_orders()
            elif choice == '13':
                client.get_order_products()
            elif choice == '14':
                client.add_product_to_order()
            elif choice == '15':
                client.remove_product_from_order()
            elif choice == '16':
                client.update_order_status()
            elif choice == '17':
                client.get_system_stats()
            elif choice == '18':
                confirm = input("This will create sample data. Continue? (y/N): ").strip().lower()
                if confirm == 'y':
                    client.run_complete_test_suite()
            else:
                print("Invalid choice. Please select 0-18.")
                
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()