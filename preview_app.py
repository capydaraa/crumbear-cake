# Simple Flask Preview App for Crumbear UI
# This is a temporary app to preview the frontend before connecting to the database

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, 
            template_folder='frontend/templates',
            static_folder='frontend/static')

# Configuration for file uploads
app.config['UPLOAD_FOLDER'] = 'frontend/static/images/cakes'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

# Mock Toppings Data
MOCK_TOPPINGS = [
    {'topping_id': 1, 'name': 'Cherry', 'price': 20.00, 'is_available': True},
    {'topping_id': 2, 'name': 'Strawberry', 'price': 25.00, 'is_available': True},
    {'topping_id': 3, 'name': 'Chocolate Chips', 'price': 15.00, 'is_available': True},
    {'topping_id': 4, 'name': 'Sprinkles', 'price': 10.00, 'is_available': True},
    {'topping_id': 5, 'name': 'Oreo Crumbs', 'price': 30.00, 'is_available': True},
    {'topping_id': 6, 'name': 'Macaron', 'price': 35.00, 'is_available': True},
    {'topping_id': 7, 'name': 'Fresh Berries', 'price': 40.00, 'is_available': True},
    {'topping_id': 8, 'name': 'Caramel Drizzle', 'price': 20.00, 'is_available': True},
    {'topping_id': 9, 'name': 'Whipped Cream', 'price': 15.00, 'is_available': True},
    {'topping_id': 10, 'name': 'Edible Flowers', 'price': 50.00, 'is_available': True},
]

# Mock Flavors Data
MOCK_FLAVORS = [
    {'flavor_id': 1, 'name': 'Chocolate', 'price_per_layer': 50.00, 'is_available': True},
    {'flavor_id': 2, 'name': 'Vanilla', 'price_per_layer': 40.00, 'is_available': True},
    {'flavor_id': 3, 'name': 'Red Velvet', 'price_per_layer': 60.00, 'is_available': True},
    {'flavor_id': 4, 'name': 'Strawberry', 'price_per_layer': 55.00, 'is_available': True},
    {'flavor_id': 5, 'name': 'Ube', 'price_per_layer': 65.00, 'is_available': True},
    {'flavor_id': 6, 'name': 'Mocha', 'price_per_layer': 55.00, 'is_available': True},
    {'flavor_id': 7, 'name': 'Lemon', 'price_per_layer': 50.00, 'is_available': True},
]

# Mock Icing Colors Data
MOCK_COLORS = [
    {'color_id': 1, 'color_name': 'Red', 'hex_code': '#FF0000', 'shade': 'Medium', 'is_available': True},
    {'color_id': 2, 'color_name': 'Pink', 'hex_code': '#FFC0CB', 'shade': 'Light', 'is_available': True},
    {'color_id': 3, 'color_name': 'Blue', 'hex_code': '#0000FF', 'shade': 'Medium', 'is_available': True},
    {'color_id': 4, 'color_name': 'Green', 'hex_code': '#00FF00', 'shade': 'Medium', 'is_available': True},
    {'color_id': 5, 'color_name': 'Yellow', 'hex_code': '#FFFF00', 'shade': 'Light', 'is_available': True},
    {'color_id': 6, 'color_name': 'Purple', 'hex_code': '#800080', 'shade': 'Dark', 'is_available': True},
    {'color_id': 7, 'color_name': 'Orange', 'hex_code': '#FFA500', 'shade': 'Medium', 'is_available': True},
    {'color_id': 8, 'color_name': 'Brown', 'hex_code': '#8B4513', 'shade': 'Dark', 'is_available': True},
    {'color_id': 9, 'color_name': 'White', 'hex_code': '#FFFFFF', 'shade': 'Light', 'is_available': True},
    {'color_id': 10, 'color_name': 'Black', 'hex_code': '#000000', 'shade': 'Dark', 'is_available': True},
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
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Temporary hardcoded credentials (TODO: Move to database)
        if username == 'admin' and password == 'crumbear123':
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid username or password')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard with analytics"""
    # Mock statistics
    stats = {
        'total_cakes': len(MOCK_CAKES),
        'total_views': sum(cake['view_count'] for cake in MOCK_CAKES),
        'total_estimates': 15,
        'featured_cakes': sum(1 for cake in MOCK_CAKES if cake['is_featured'])
    }
    
    # Top 10 cakes by views
    top_cakes = sorted(MOCK_CAKES, key=lambda x: x['view_count'], reverse=True)[:10]
    
    # Chart data
    chart_data = {
        'cake_names': [cake['name'] for cake in top_cakes[:5]],
        'cake_views': [cake['view_count'] for cake in top_cakes[:5]],
        'categories': ['Birthday', 'Wedding', 'Anniversaries', 'Cartoons', 'Other'],
        'category_counts': [
            sum(1 for cake in MOCK_CAKES if cake['category'] == 'Birthday'),
            sum(1 for cake in MOCK_CAKES if cake['category'] == 'Wedding'),
            sum(1 for cake in MOCK_CAKES if cake['category'] == 'Anniversaries'),
            sum(1 for cake in MOCK_CAKES if cake['category'] == 'Cartoons'),
            sum(1 for cake in MOCK_CAKES if cake['category'] == 'Other'),
        ]
    }
    
    return render_template('admin_dashboard.html', stats=stats, top_cakes=top_cakes, chart_data=chart_data)

@app.route('/admin/cakes')
def admin_cakes():
    """Admin cakes management page"""
    # Add images array to each cake for the template
    cakes_with_images = []
    for cake in MOCK_CAKES:
        cake_copy = cake.copy()
        cake_copy['images'] = [{'image_url': cake['image_url'], 'is_primary': True}]
        cakes_with_images.append(cake_copy)
    return render_template('admin_cakes.html', cakes=cakes_with_images)

@app.route('/admin/cakes/add', methods=['POST'])
def admin_add_cake():
    """Add new cake"""
    try:
        # Get form data
        name = request.form.get('name')
        description = request.form.get('description', '')
        category = request.form.get('category')
        base_price_4x3 = float(request.form.get('base_price_4x3'))
        base_price_5x3 = float(request.form.get('base_price_5x3'))
        base_price_6x3 = float(request.form.get('base_price_6x3'))
        is_featured = request.form.get('is_featured') == '1'
        
        # Generate new cake ID
        new_id = max([cake['cake_id'] for cake in MOCK_CAKES]) + 1 if MOCK_CAKES else 1
        
        # Handle file upload
        image_url = 'https://images.unsplash.com/photo-1558636508-e0db3814bd1d?w=800&q=80'  # Default
        if 'images' in request.files:
            files = request.files.getlist('images')
            if files and files[0].filename != '':
                file = files[0]  # Use first image as primary
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"cake_{new_id}_{file.filename}")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    image_url = url_for('static', filename=f'images/cakes/{filename}')
        
        # Create new cake
        new_cake = {
            'cake_id': new_id,
            'name': name,
            'description': description,
            'category': category,
            'image_url': image_url,
            'base_price_4x3': base_price_4x3,
            'base_price_5x3': base_price_5x3,
            'base_price_6x3': base_price_6x3,
            'is_featured': is_featured,
            'view_count': 0
        }
        
        MOCK_CAKES.append(new_cake)
        print(f"✅ Added new cake: {name}")
        return redirect(url_for('admin_cakes'))
    except Exception as e:
        print(f"❌ Error adding cake: {e}")
        return redirect(url_for('admin_cakes'))

@app.route('/admin/cakes/edit/<int:cake_id>', methods=['POST'])
def admin_edit_cake(cake_id):
    """Edit existing cake"""
    try:
        # Find the cake
        cake = next((c for c in MOCK_CAKES if c['cake_id'] == cake_id), None)
        if not cake:
            return jsonify({'success': False, 'message': 'Cake not found'}), 404
        
        # Update cake data
        cake['name'] = request.form.get('name')
        cake['description'] = request.form.get('description', '')
        cake['category'] = request.form.get('category')
        cake['base_price_4x3'] = float(request.form.get('base_price_4x3'))
        cake['base_price_5x3'] = float(request.form.get('base_price_5x3'))
        cake['base_price_6x3'] = float(request.form.get('base_price_6x3'))
        cake['is_featured'] = request.form.get('is_featured') == '1'
        
        # Handle file upload if new images provided
        if 'images' in request.files:
            files = request.files.getlist('images')
            if files and files[0].filename != '':
                file = files[0]
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"cake_{cake_id}_{file.filename}")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    cake['image_url'] = url_for('static', filename=f'images/cakes/{filename}')
        
        print(f"✅ Updated cake ID {cake_id}: {cake['name']}")
        return redirect(url_for('admin_cakes'))
    except Exception as e:
        print(f"❌ Error editing cake: {e}")
        return redirect(url_for('admin_cakes'))

@app.route('/admin/cakes/delete/<int:cake_id>', methods=['POST'])
def admin_delete_cake(cake_id):
    """Delete cake"""
    try:
        global MOCK_CAKES
        cake = next((c for c in MOCK_CAKES if c['cake_id'] == cake_id), None)
        if cake:
            MOCK_CAKES = [c for c in MOCK_CAKES if c['cake_id'] != cake_id]
            print(f"✅ Deleted cake ID {cake_id}: {cake['name']}")
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Cake not found'}), 404
    except Exception as e:
        print(f"❌ Error deleting cake: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/toppings')
def admin_toppings():
    """Admin toppings management page"""
    return render_template('admin_toppings.html', toppings=MOCK_TOPPINGS)

@app.route('/admin/toppings/add', methods=['POST'])
def admin_add_topping():
    """Add new topping"""
    try:
        name = request.form.get('name')
        price = float(request.form.get('price'))
        is_available = request.form.get('is_available') == '1'
        
        new_id = max([t['topping_id'] for t in MOCK_TOPPINGS]) + 1 if MOCK_TOPPINGS else 1
        new_topping = {
            'topping_id': new_id,
            'name': name,
            'price': price,
            'is_available': is_available
        }
        MOCK_TOPPINGS.append(new_topping)
        print(f"✅ Added topping: {name}")
        return redirect(url_for('admin_toppings'))
    except Exception as e:
        print(f"❌ Error adding topping: {e}")
        return redirect(url_for('admin_toppings'))

@app.route('/admin/toppings/edit/<int:topping_id>', methods=['POST'])
def admin_edit_topping(topping_id):
    """Edit existing topping"""
    try:
        topping = next((t for t in MOCK_TOPPINGS if t['topping_id'] == topping_id), None)
        if topping:
            topping['name'] = request.form.get('name')
            topping['price'] = float(request.form.get('price'))
            topping['is_available'] = request.form.get('is_available') == '1'
            print(f"✅ Updated topping ID {topping_id}")
            return redirect(url_for('admin_toppings'))
        return jsonify({'success': False, 'message': 'Topping not found'}), 404
    except Exception as e:
        print(f"❌ Error editing topping: {e}")
        return redirect(url_for('admin_toppings'))

@app.route('/admin/toppings/delete/<int:topping_id>', methods=['POST'])
def admin_delete_topping(topping_id):
    """Delete topping"""
    try:
        global MOCK_TOPPINGS
        topping = next((t for t in MOCK_TOPPINGS if t['topping_id'] == topping_id), None)
        if topping:
            MOCK_TOPPINGS = [t for t in MOCK_TOPPINGS if t['topping_id'] != topping_id]
            print(f"✅ Deleted topping ID {topping_id}")
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Topping not found'}), 404
    except Exception as e:
        print(f"❌ Error deleting topping: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/flavors')
def admin_flavors():
    """Admin flavors management page"""
    return render_template('admin_flavors.html', flavors=MOCK_FLAVORS)

@app.route('/admin/flavors/add', methods=['POST'])
def admin_add_flavor():
    """Add new flavor"""
    try:
        name = request.form.get('name')
        price_per_layer = float(request.form.get('price_per_layer'))
        is_available = request.form.get('is_available') == '1'
        
        new_id = max([f['flavor_id'] for f in MOCK_FLAVORS]) + 1 if MOCK_FLAVORS else 1
        new_flavor = {
            'flavor_id': new_id,
            'name': name,
            'price_per_layer': price_per_layer,
            'is_available': is_available
        }
        MOCK_FLAVORS.append(new_flavor)
        print(f"✅ Added flavor: {name}")
        return redirect(url_for('admin_flavors'))
    except Exception as e:
        print(f"❌ Error adding flavor: {e}")
        return redirect(url_for('admin_flavors'))

@app.route('/admin/flavors/edit/<int:flavor_id>', methods=['POST'])
def admin_edit_flavor(flavor_id):
    """Edit existing flavor"""
    try:
        flavor = next((f for f in MOCK_FLAVORS if f['flavor_id'] == flavor_id), None)
        if flavor:
            flavor['name'] = request.form.get('name')
            flavor['price_per_layer'] = float(request.form.get('price_per_layer'))
            flavor['is_available'] = request.form.get('is_available') == '1'
            print(f"✅ Updated flavor ID {flavor_id}")
            return redirect(url_for('admin_flavors'))
        return jsonify({'success': False, 'message': 'Flavor not found'}), 404
    except Exception as e:
        print(f"❌ Error editing flavor: {e}")
        return redirect(url_for('admin_flavors'))

@app.route('/admin/flavors/delete/<int:flavor_id>', methods=['POST'])
def admin_delete_flavor(flavor_id):
    """Delete flavor"""
    try:
        global MOCK_FLAVORS
        flavor = next((f for f in MOCK_FLAVORS if f['flavor_id'] == flavor_id), None)
        if flavor:
            MOCK_FLAVORS = [f for f in MOCK_FLAVORS if f['flavor_id'] != flavor_id]
            print(f"✅ Deleted flavor ID {flavor_id}")
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Flavor not found'}), 404
    except Exception as e:
        print(f"❌ Error deleting flavor: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/colors')
def admin_colors():
    """Admin colors management page"""
    return render_template('admin_colors.html', colors=MOCK_COLORS)

@app.route('/admin/colors/add', methods=['POST'])
def admin_add_color():
    """Add new color"""
    try:
        color_name = request.form.get('color_name')
        hex_code = request.form.get('hex_code')
        shade = request.form.get('shade')
        is_available = request.form.get('is_available') == '1'
        
        new_id = max([c['color_id'] for c in MOCK_COLORS]) + 1 if MOCK_COLORS else 1
        new_color = {
            'color_id': new_id,
            'color_name': color_name,
            'hex_code': hex_code,
            'shade': shade,
            'is_available': is_available
        }
        MOCK_COLORS.append(new_color)
        print(f"✅ Added color: {color_name}")
        return redirect(url_for('admin_colors'))
    except Exception as e:
        print(f"❌ Error adding color: {e}")
        return redirect(url_for('admin_colors'))

@app.route('/admin/colors/edit/<int:color_id>', methods=['POST'])
def admin_edit_color(color_id):
    """Edit existing color"""
    try:
        color = next((c for c in MOCK_COLORS if c['color_id'] == color_id), None)
        if color:
            color['color_name'] = request.form.get('color_name')
            color['hex_code'] = request.form.get('hex_code')
            color['shade'] = request.form.get('shade')
            color['is_available'] = request.form.get('is_available') == '1'
            print(f"✅ Updated color ID {color_id}")
            return redirect(url_for('admin_colors'))
        return jsonify({'success': False, 'message': 'Color not found'}), 404
    except Exception as e:
        print(f"❌ Error editing color: {e}")
        return redirect(url_for('admin_colors'))

@app.route('/admin/colors/delete/<int:color_id>', methods=['POST'])
def admin_delete_color(color_id):
    """Delete color"""
    try:
        global MOCK_COLORS
        color = next((c for c in MOCK_COLORS if c['color_id'] == color_id), None)
        if color:
            MOCK_COLORS = [c for c in MOCK_COLORS if c['color_id'] != color_id]
            print(f"✅ Deleted color ID {color_id}")
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Color not found'}), 404
    except Exception as e:
        print(f"❌ Error deleting color: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

# API endpoints (mock data for testing)
@app.route('/api/cakes')
def api_cakes():
    """Get all cakes"""
    return jsonify(MOCK_CAKES)

@app.route('/api/cakes/<int:cake_id>')
def api_cake_detail(cake_id):
    """Get single cake by ID"""
    cake = next((c for c in MOCK_CAKES if c['cake_id'] == cake_id), None)
    if cake:
        cake_with_images = cake.copy()
        cake_with_images['images'] = [{'image_url': cake['image_url'], 'is_primary': True}]
        return jsonify(cake_with_images)
    return jsonify({'error': 'Cake not found'}), 404

@app.route('/api/flavors')
def api_flavors():
    """Get all flavors"""
    return jsonify(MOCK_FLAVORS)

@app.route('/api/toppings')
def api_toppings():
    """Get all toppings"""
    return jsonify(MOCK_TOPPINGS)

@app.route('/api/colors')
def api_colors():
    """Get all icing colors"""
    return jsonify(MOCK_COLORS)

@app.route('/api/estimates', methods=['POST'])
def api_save_estimate():
    """Save price estimate"""
    data = request.json
    print("Estimate saved:", data)
    return jsonify({'success': True, 'estimate_id': 1})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
