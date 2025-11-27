# Simple Flask Preview App for Crumbear UI
# This is a temporary app to preview the frontend before connecting to the database

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

app = Flask(__name__, 
            template_folder='frontend/templates',
            static_folder='frontend/static')

# Mock data for preview with stock images
MOCK_CAKES = [
    {
        'cake_id': 1,
        'name': 'Strawberry Dream',
        'description': 'A delicious strawberry cake with fresh berries',
        'category': 'Birthday',
        'image_url': 'https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=800&q=80',
        'base_price_4x3': 350,
        'base_price_5x3': 500,
        'base_price_6x3': 650,
        'is_featured': True,
        'view_count': 42
    },
    {
        'cake_id': 2,
        'name': 'Chocolate Paradise',
        'description': 'Rich chocolate cake with chocolate ganache',
        'category': 'Birthday',
        'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
        'base_price_4x3': 400,
        'base_price_5x3': 550,
        'base_price_6x3': 700,
        'is_featured': False,
        'view_count': 38
    },
    {
        'cake_id': 3,
        'name': 'Elegant White',
        'description': 'Classic white wedding cake with delicate details',
        'category': 'Wedding',
        'image_url': 'https://images.unsplash.com/photo-1535254973040-607b474cb50d?w=800&q=80',
        'base_price_4x3': 500,
        'base_price_5x3': 700,
        'base_price_6x3': 900,
        'is_featured': True,
        'view_count': 56
    },
    {
        'cake_id': 4,
        'name': 'Golden Anniversary',
        'description': 'Luxurious gold-themed anniversary cake',
        'category': 'Anniversaries',
        'image_url': 'https://images.unsplash.com/photo-1588195538326-c5b1e5b491e9?w=800&q=80',
        'base_price_4x3': 450,
        'base_price_5x3': 600,
        'base_price_6x3': 750,
        'is_featured': False,
        'view_count': 29
    },
    {
        'cake_id': 5,
        'name': 'Unicorn Magic',
        'description': 'Colorful unicorn-themed cake for kids',
        'category': 'Cartoons',
        'image_url': 'https://images.unsplash.com/photo-1558636508-e0db3814bd1d?w=800&q=80',
        'base_price_4x3': 450,
        'base_price_5x3': 600,
        'base_price_6x3': 800,
        'is_featured': True,
        'view_count': 67
    },
    {
        'cake_id': 6,
        'name': 'Bear Hug Cake',
        'description': 'Adorable bear-themed design',
        'category': 'Cartoons',
        'image_url': 'https://images.unsplash.com/photo-1621303837174-89787a7d4729?w=800&q=80',
        'base_price_4x3': 420,
        'base_price_5x3': 580,
        'base_price_6x3': 750,
        'is_featured': False,
        'view_count': 45
    }
]

@app.route('/')
def index():
    """Home page - Browse cakes"""
    return render_template('index.html', cakes=MOCK_CAKES)

@app.route('/calculator')
def calculator():
    """Price calculator page"""
    return render_template('calculator.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        # Mock login - just redirect for now
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard (placeholder)"""
    return "<h1>Admin Dashboard Coming Soon!</h1><a href='/'>Back to Home</a>"

# API endpoints (mock data for testing)
@app.route('/api/cakes')
def api_cakes():
    """Get all cakes"""
    return jsonify(MOCK_CAKES)

@app.route('/api/flavors')
def api_flavors():
    """Get all flavors"""
    mock_flavors = [
        {'flavor_id': 1, 'name': 'Chocolate', 'price_per_layer': 50, 'is_available': True},
        {'flavor_id': 2, 'name': 'Vanilla', 'price_per_layer': 40, 'is_available': True},
        {'flavor_id': 3, 'name': 'Red Velvet', 'price_per_layer': 60, 'is_available': True},
        {'flavor_id': 4, 'name': 'Strawberry', 'price_per_layer': 55, 'is_available': True},
        {'flavor_id': 5, 'name': 'Ube', 'price_per_layer': 65, 'is_available': True},
    ]
    return jsonify(mock_flavors)

@app.route('/api/toppings')
def api_toppings():
    """Get all toppings"""
    mock_toppings = [
        {'topping_id': 1, 'name': 'Cherry', 'price': 20, 'is_available': True},
        {'topping_id': 2, 'name': 'Strawberry', 'price': 25, 'is_available': True},
        {'topping_id': 3, 'name': 'Chocolate Chips', 'price': 15, 'is_available': True},
        {'topping_id': 4, 'name': 'Sprinkles', 'price': 10, 'is_available': True},
        {'topping_id': 5, 'name': 'Oreo Crumbs', 'price': 30, 'is_available': True},
        {'topping_id': 6, 'name': 'Macaron', 'price': 35, 'is_available': True},
        {'topping_id': 7, 'name': 'Fresh Berries', 'price': 40, 'is_available': True},
        {'topping_id': 8, 'name': 'Caramel Drizzle', 'price': 20, 'is_available': True},
        {'topping_id': 9, 'name': 'Whipped Cream', 'price': 15, 'is_available': True},
        {'topping_id': 10, 'name': 'Edible Flowers', 'price': 50, 'is_available': True},
    ]
    return jsonify(mock_toppings)

@app.route('/api/colors')
def api_colors():
    """Get all icing colors"""
    mock_colors = [
        {'color_id': 1, 'color_name': 'Red', 'hex_code': '#FF0000'},
        {'color_id': 2, 'color_name': 'Pink', 'hex_code': '#FFC0CB'},
        {'color_id': 3, 'color_name': 'Blue', 'hex_code': '#0000FF'},
        {'color_id': 4, 'color_name': 'Green', 'hex_code': '#00FF00'},
        {'color_id': 5, 'color_name': 'Yellow', 'hex_code': '#FFFF00'},
        {'color_id': 6, 'color_name': 'Purple', 'hex_code': '#800080'},
        {'color_id': 7, 'color_name': 'Orange', 'hex_code': '#FFA500'},
        {'color_id': 8, 'color_name': 'Brown', 'hex_code': '#8B4513'},
        {'color_id': 9, 'color_name': 'White', 'hex_code': '#FFFFFF'},
        {'color_id': 10, 'color_name': 'Black', 'hex_code': '#000000'},
    ]
    return jsonify(mock_colors)

@app.route('/api/estimates', methods=['POST'])
def api_save_estimate():
    """Save price estimate"""
    data = request.json
    print("Estimate saved:", data)
    return jsonify({'success': True, 'estimate_id': 1})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
