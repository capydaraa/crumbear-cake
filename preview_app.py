# Crumbear Cake Management System - Preview App
# Flask application with mock data for the new normalized schema
# Tables: Cakes, CakeDesigns, Customers, Reviews

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import random

app = Flask(__name__, 
            template_folder='frontend/templates',
            static_folder='frontend/static')

# Configuration
app.config['UPLOAD_FOLDER'] = 'frontend/static/images/cakes'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = 'crumbear_secret_key_2024'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
DATA_FILE = 'data/crumbear_data.json'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('data', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==============================================================================
# DATA PERSISTENCE - Save and Load from JSON file
# ==============================================================================

# Default data if no saved data exists
DEFAULT_CAKES = [
    {'cake_id': 1, 'cake_name': 'Classic Vanilla Cake', 'flavor': 'Vanilla', 'frosting': 'Buttercream', 'size': '8 inch', 'base_price': 45.00, 'availability': True, 'created_at': '2025-12-01'},
    {'cake_id': 2, 'cake_name': 'Rich Chocolate Cake', 'flavor': 'Chocolate', 'frosting': 'Ganache', 'size': '8 inch', 'base_price': 50.00, 'availability': True, 'created_at': '2025-12-05'},
    {'cake_id': 3, 'cake_name': 'Red Velvet Delight', 'flavor': 'Red Velvet', 'frosting': 'Cream Cheese', 'size': '10 inch', 'base_price': 65.00, 'availability': True, 'created_at': '2025-12-10'},
    {'cake_id': 4, 'cake_name': 'Lemon Zest Cake', 'flavor': 'Lemon', 'frosting': 'Buttercream', 'size': '6 inch', 'base_price': 35.00, 'availability': True, 'created_at': '2025-12-12'},
    {'cake_id': 5, 'cake_name': 'Strawberry Dream', 'flavor': 'Strawberry', 'frosting': 'Whipped Cream', 'size': '8 inch', 'base_price': 48.00, 'availability': True, 'created_at': '2025-12-15'},
    {'cake_id': 6, 'cake_name': 'Carrot Spice Cake', 'flavor': 'Carrot', 'frosting': 'Cream Cheese', 'size': '10 inch', 'base_price': 55.00, 'availability': False, 'created_at': '2025-12-18'},
]

DEFAULT_DESIGNS = [
    {'design_id': 1, 'cake_id': 1, 'theme': 'Birthday Party', 'color_palette': 'Pink & White', 'topper_type': 'Candles', 'complexity_level': 'Simple', 'image_url': 'https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=800&q=80', 'created_at': '2025-12-02'},
    {'design_id': 2, 'cake_id': 1, 'theme': 'Floral Garden', 'color_palette': 'Pastel Rainbow', 'topper_type': 'Fresh Flowers', 'complexity_level': 'Moderate', 'image_url': 'https://images.unsplash.com/photo-1535254973040-607b474cb50d?w=800&q=80', 'created_at': '2025-12-03'},
    {'design_id': 3, 'cake_id': 2, 'theme': 'Modern Minimalist', 'color_palette': 'Black & White', 'topper_type': 'Chocolate Decorations', 'complexity_level': 'Moderate', 'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80', 'created_at': '2025-12-06'},
    {'design_id': 4, 'cake_id': 2, 'theme': 'Rustic Charm', 'color_palette': 'Green & Brown', 'topper_type': 'Berries', 'complexity_level': 'Complex', 'image_url': 'https://images.unsplash.com/photo-1621303837174-89787a7d4729?w=800&q=80', 'created_at': '2025-12-07'},
    {'design_id': 5, 'cake_id': 3, 'theme': 'Wedding Elegant', 'color_palette': 'Gold & Ivory', 'topper_type': 'Cake Topper Sign', 'complexity_level': 'Expert', 'image_url': 'https://images.unsplash.com/photo-1588195538326-c5b1e5b491e9?w=800&q=80', 'created_at': '2025-12-11'},
    {'design_id': 6, 'cake_id': 4, 'theme': 'Spring Fresh', 'color_palette': 'Yellow & White', 'topper_type': 'Fresh Flowers', 'complexity_level': 'Simple', 'image_url': 'https://images.unsplash.com/photo-1558636508-e0db3814bd1d?w=800&q=80', 'created_at': '2025-12-13'},
    {'design_id': 7, 'cake_id': 5, 'theme': 'Princess Fantasy', 'color_palette': 'Pink & White', 'topper_type': 'Fondant Figures', 'complexity_level': 'Complex', 'image_url': 'https://images.unsplash.com/photo-1562777717-dc6984f65a63?w=800&q=80', 'created_at': '2025-12-16'},
    {'design_id': 8, 'cake_id': 5, 'theme': 'Unicorn Magic', 'color_palette': 'Pastel Rainbow', 'topper_type': 'Custom Figurine', 'complexity_level': 'Expert', 'image_url': 'https://images.unsplash.com/photo-1557979619-445218f326b9?w=800&q=80', 'created_at': '2025-12-17'},
]

DEFAULT_CUSTOMERS = [
    {'customer_id': 1, 'full_name': 'Emma Johnson', 'email': 'emma.johnson@email.com', 'city': 'New York', 'created_at': '2025-11-01'},
    {'customer_id': 2, 'full_name': 'Liam Smith', 'email': 'liam.smith@email.com', 'city': 'Los Angeles', 'created_at': '2025-11-05'},
    {'customer_id': 3, 'full_name': 'Olivia Brown', 'email': 'olivia.brown@email.com', 'city': 'Chicago', 'created_at': '2025-11-10'},
    {'customer_id': 4, 'full_name': 'Noah Davis', 'email': 'noah.davis@email.com', 'city': 'Houston', 'created_at': '2025-11-15'},
    {'customer_id': 5, 'full_name': 'Ava Wilson', 'email': 'ava.wilson@email.com', 'city': 'Phoenix', 'created_at': '2025-11-20'},
    {'customer_id': 6, 'full_name': 'Sophia Garcia', 'email': 'sophia.garcia@email.com', 'city': 'Miami', 'created_at': '2025-11-25'},
]

DEFAULT_REVIEWS = [
    {'review_id': 1, 'customer_id': 1, 'design_id': 1, 'rating': 5, 'review_text': 'Absolutely perfect for my daughter\'s birthday!', 'review_date': '2025-12-05'},
    {'review_id': 2, 'customer_id': 2, 'design_id': 3, 'rating': 4, 'review_text': 'Beautiful design, great chocolate flavor.', 'review_date': '2025-12-08'},
    {'review_id': 3, 'customer_id': 3, 'design_id': 5, 'rating': 5, 'review_text': 'The wedding cake was stunning!', 'review_date': '2025-12-12'},
    {'review_id': 4, 'customer_id': 4, 'design_id': 2, 'rating': 4, 'review_text': 'Lovely floral design, tasted amazing.', 'review_date': '2025-12-14'},
    {'review_id': 5, 'customer_id': 5, 'design_id': 7, 'rating': 5, 'review_text': 'My daughter loved the princess cake!', 'review_date': '2025-12-18'},
    {'review_id': 6, 'customer_id': 6, 'design_id': 4, 'rating': 3, 'review_text': 'Good cake but delivery was late.', 'review_date': '2025-12-20'},
    {'review_id': 7, 'customer_id': 1, 'design_id': 8, 'rating': 5, 'review_text': 'The unicorn design was magical!', 'review_date': '2025-12-22'},
    {'review_id': 8, 'customer_id': 2, 'design_id': 6, 'rating': 4, 'review_text': 'Fresh and delicious lemon cake.', 'review_date': '2025-12-24'},
]

def load_data():
    """Load data from JSON file, or use defaults if file doesn't exist"""
    global MOCK_CAKES, MOCK_DESIGNS, MOCK_CUSTOMERS, MOCK_REVIEWS
    
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                MOCK_CAKES = data.get('cakes', DEFAULT_CAKES)
                MOCK_DESIGNS = data.get('designs', DEFAULT_DESIGNS)
                MOCK_CUSTOMERS = data.get('customers', DEFAULT_CUSTOMERS)
                MOCK_REVIEWS = data.get('reviews', DEFAULT_REVIEWS)
                print(f"✅ Loaded data from {DATA_FILE}")
                return
        except Exception as e:
            print(f"⚠️ Error loading data: {e}, using defaults")
    
    # Use defaults
    MOCK_CAKES = DEFAULT_CAKES.copy()
    MOCK_DESIGNS = DEFAULT_DESIGNS.copy()
    MOCK_CUSTOMERS = DEFAULT_CUSTOMERS.copy()
    MOCK_REVIEWS = DEFAULT_REVIEWS.copy()
    save_data()  # Save defaults

def save_data():
    """Save current data to JSON file"""
    try:
        data = {
            'cakes': MOCK_CAKES,
            'designs': MOCK_DESIGNS,
            'customers': MOCK_CUSTOMERS,
            'reviews': MOCK_REVIEWS
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Data saved to {DATA_FILE}")
    except Exception as e:
        print(f"❌ Error saving data: {e}")

# Initialize data lists (will be populated by load_data)
MOCK_CAKES = []
MOCK_DESIGNS = []
MOCK_CUSTOMERS = []
MOCK_REVIEWS = []

# Load data on startup
load_data()

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def get_design_with_details(design):
    """Add cake info and ratings to a design"""
    cake = next((c for c in MOCK_CAKES if c['cake_id'] == design['cake_id']), None)
    reviews = [r for r in MOCK_REVIEWS if r['design_id'] == design['design_id']]
    avg_rating = sum(r['rating'] for r in reviews) / len(reviews) if reviews else 0
    
    return {
        **design,
        'cake_name': cake['cake_name'] if cake else 'Unknown',
        'flavor': cake['flavor'] if cake else 'Unknown',
        'base_price': cake['base_price'] if cake else 0,
        'avg_rating': round(avg_rating, 1),
        'review_count': len(reviews),
        'calculated_price': calculate_design_price(design, cake)
    }

def calculate_design_price(design, cake):
    """Calculate price based on complexity"""
    if not cake:
        return 0
    multiplier = {
        'Simple': 1.0,
        'Moderate': 1.25,
        'Complex': 1.5,
        'Expert': 2.0
    }.get(design['complexity_level'], 1.0)
    return round(cake['base_price'] * multiplier, 2)

def get_customer_with_stats(customer):
    """Add review stats to customer"""
    reviews = [r for r in MOCK_REVIEWS if r['customer_id'] == customer['customer_id']]
    avg_rating = sum(r['rating'] for r in reviews) / len(reviews) if reviews else 0
    return {
        **customer,
        'total_reviews': len(reviews),
        'avg_rating_given': round(avg_rating, 1)
    }

# ==============================================================================
# SESSION - Logged in customer tracking
# ==============================================================================
LOGGED_IN_CUSTOMER = None  # Simple session simulation

# ==============================================================================
# PUBLIC ROUTES
# ==============================================================================

@app.route('/')
def index():
    """Home page - Browse cake designs"""
    global LOGGED_IN_CUSTOMER
    designs_with_details = [get_design_with_details(d) for d in MOCK_DESIGNS]
    return render_template('index.html', designs=designs_with_details, cakes=MOCK_CAKES, logged_in_customer=LOGGED_IN_CUSTOMER)

@app.route('/design/<int:design_id>')
def design_detail(design_id):
    """Design detail page with reviews"""
    global LOGGED_IN_CUSTOMER
    design = next((d for d in MOCK_DESIGNS if d['design_id'] == design_id), None)
    if not design:
        return redirect(url_for('index'))
    
    design_with_details = get_design_with_details(design)
    
    # Get cake details for this design
    cake = next((c for c in MOCK_CAKES if c['cake_id'] == design['cake_id']), None)
    if cake:
        design_with_details['frosting'] = cake['frosting']
        design_with_details['size'] = cake['size']
    
    # Get reviews for this design with customer info
    reviews = []
    for r in MOCK_REVIEWS:
        if r['design_id'] == design_id:
            customer = next((c for c in MOCK_CUSTOMERS if c['customer_id'] == r['customer_id']), None)
            reviews.append({
                **r,
                'customer_name': customer['full_name'] if customer else 'Anonymous',
                'city': customer['city'] if customer else ''
            })
    
    return render_template('design_detail.html', 
                           design=design_with_details, 
                           reviews=reviews,
                           logged_in_customer=LOGGED_IN_CUSTOMER)

@app.route('/calculator')
def calculator():
    """Price calculator page"""
    global LOGGED_IN_CUSTOMER
    return render_template('calculator.html', cakes=MOCK_CAKES, logged_in_customer=LOGGED_IN_CUSTOMER)

# ==============================================================================
# CUSTOMER AUTHENTICATION
# ==============================================================================

@app.route('/login', methods=['GET', 'POST'])
def customer_login():
    """Customer login page"""
    global LOGGED_IN_CUSTOMER
    next_url = request.args.get('next', '')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        next_url = request.form.get('next', '')
        
        # Simple auth: check if email exists in customers (password: 'password123' for all)
        customer = next((c for c in MOCK_CUSTOMERS if c['email'] == email), None)
        if customer and password == 'password123':
            LOGGED_IN_CUSTOMER = customer
            if next_url:
                return redirect(next_url)
            return redirect(url_for('index'))
        return render_template('customer_auth.html', error='Invalid email or password', next_url=next_url)
    
    return render_template('customer_auth.html', next_url=next_url)

@app.route('/signup', methods=['POST'])
def customer_signup():
    """Customer signup"""
    global LOGGED_IN_CUSTOMER, MOCK_CUSTOMERS
    
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    city = request.form.get('city')
    password = request.form.get('password')
    next_url = request.form.get('next', '')
    
    # Check if email already exists
    if any(c['email'] == email for c in MOCK_CUSTOMERS):
        return render_template('customer_auth.html', error='Email already registered', next_url=next_url)
    
    # Create new customer
    new_id = max(c['customer_id'] for c in MOCK_CUSTOMERS) + 1
    new_customer = {
        'customer_id': new_id,
        'full_name': full_name,
        'email': email,
        'city': city,
        'created_at': datetime.now().strftime('%Y-%m-%d')
    }
    MOCK_CUSTOMERS.append(new_customer)
    save_data()  # Persist to file
    LOGGED_IN_CUSTOMER = new_customer
    
    if next_url:
        return redirect(next_url)
    return redirect(url_for('index'))

@app.route('/logout')
def customer_logout():
    """Customer logout"""
    global LOGGED_IN_CUSTOMER
    LOGGED_IN_CUSTOMER = None
    return redirect(url_for('index'))

@app.route('/review/<int:design_id>', methods=['POST'])
def submit_review(design_id):
    """Submit a review for a design"""
    global LOGGED_IN_CUSTOMER, MOCK_REVIEWS
    
    if not LOGGED_IN_CUSTOMER:
        return redirect(url_for('customer_login', next=url_for('design_detail', design_id=design_id)))
    
    rating = int(request.form.get('rating', 5))
    review_text = request.form.get('review_text', '')
    
    new_id = max(r['review_id'] for r in MOCK_REVIEWS) + 1
    new_review = {
        'review_id': new_id,
        'customer_id': LOGGED_IN_CUSTOMER['customer_id'],
        'design_id': design_id,
        'rating': rating,
        'review_text': review_text,
        'review_date': datetime.now().strftime('%Y-%m-%d')
    }
    MOCK_REVIEWS.append(new_review)
    save_data()  # Persist to file
    
    return redirect(url_for('design_detail', design_id=design_id))

# ==============================================================================
# ADMIN AUTHENTICATION
# ==============================================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'crumbear123':
            return redirect(url_for('admin_dashboard'))
        return render_template('admin_login.html', error='Invalid credentials')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout - redirect to homepage"""
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard with statistics"""
    # Calculate statistics
    total_reviews = len(MOCK_REVIEWS)
    avg_rating = sum(r['rating'] for r in MOCK_REVIEWS) / total_reviews if total_reviews else 0
    
    stats = {
        'total_cakes': len(MOCK_CAKES),
        'total_designs': len(MOCK_DESIGNS),
        'total_customers': len(MOCK_CUSTOMERS),
        'total_reviews': total_reviews,
        'avg_rating': round(avg_rating, 2),
        'available_cakes': sum(1 for c in MOCK_CAKES if c['availability'])
    }
    
    # Get top designs by rating
    designs_with_ratings = [get_design_with_details(d) for d in MOCK_DESIGNS]
    top_designs = sorted(designs_with_ratings, key=lambda x: (x['avg_rating'], x['review_count']), reverse=True)[:5]
    
    # Chart data
    chart_data = {
        'design_themes': list(set(d['theme'] for d in MOCK_DESIGNS))[:5],
        'theme_counts': [sum(1 for d in MOCK_DESIGNS if d['theme'] == theme) for theme in list(set(d['theme'] for d in MOCK_DESIGNS))[:5]],
        'complexity_levels': ['Simple', 'Moderate', 'Complex', 'Expert'],
        'complexity_counts': [
            sum(1 for d in MOCK_DESIGNS if d['complexity_level'] == level)
            for level in ['Simple', 'Moderate', 'Complex', 'Expert']
        ],
        'rating_distribution': [
            sum(1 for r in MOCK_REVIEWS if r['rating'] == i) for i in range(1, 6)
        ],
        'cities': list(set(c['city'] for c in MOCK_CUSTOMERS)),
        'city_counts': [sum(1 for c in MOCK_CUSTOMERS if c['city'] == city) for city in list(set(c['city'] for c in MOCK_CUSTOMERS))]
    }
    
    return render_template('admin_dashboard.html', stats=stats, top_designs=top_designs, chart_data=chart_data)

# ==============================================================================
# ADMIN CAKES CRUD
# ==============================================================================

@app.route('/admin/cakes')
def admin_cakes():
    """Admin cakes management"""
    cakes_with_counts = []
    for cake in MOCK_CAKES:
        design_count = sum(1 for d in MOCK_DESIGNS if d['cake_id'] == cake['cake_id'])
        cakes_with_counts.append({**cake, 'design_count': design_count})
    return render_template('admin_cakes.html', cakes=cakes_with_counts)

@app.route('/admin/cakes/add', methods=['POST'])
def admin_add_cake():
    """Add new cake"""
    try:
        new_id = max([c['cake_id'] for c in MOCK_CAKES]) + 1 if MOCK_CAKES else 1
        new_cake = {
            'cake_id': new_id,
            'cake_name': request.form.get('cake_name'),
            'flavor': request.form.get('flavor'),
            'frosting': request.form.get('frosting'),
            'size': request.form.get('size'),
            'base_price': float(request.form.get('base_price')),
            'availability': request.form.get('availability') == '1',
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        MOCK_CAKES.append(new_cake)
        save_data()  # Persist to file
        print(f"✅ Added cake: {new_cake['cake_name']}")
        return redirect(url_for('admin_cakes') + '?success=Cake added successfully!')
    except Exception as e:
        print(f"❌ Error: {e}")
        return redirect(url_for('admin_cakes') + f'?error={str(e)}')

@app.route('/admin/cakes/edit/<int:cake_id>', methods=['POST'])
def admin_edit_cake(cake_id):
    """Edit cake"""
    try:
        cake = next((c for c in MOCK_CAKES if c['cake_id'] == cake_id), None)
        if cake:
            cake['cake_name'] = request.form.get('cake_name')
            cake['flavor'] = request.form.get('flavor')
            cake['frosting'] = request.form.get('frosting')
            cake['size'] = request.form.get('size')
            cake['base_price'] = float(request.form.get('base_price'))
            cake['availability'] = request.form.get('availability') == '1'
            save_data()  # Persist to file
            print(f"✅ Updated cake ID {cake_id}")
            return redirect(url_for('admin_cakes') + '?success=Cake updated successfully!')
        return redirect(url_for('admin_cakes') + '?error=Cake not found')
    except Exception as e:
        return redirect(url_for('admin_cakes') + f'?error={str(e)}')

@app.route('/admin/cakes/delete/<int:cake_id>', methods=['POST'])
def admin_delete_cake(cake_id):
    """Delete cake"""
    try:
        global MOCK_CAKES, MOCK_DESIGNS, MOCK_REVIEWS
        # Check for reviews on designs
        design_ids = [d['design_id'] for d in MOCK_DESIGNS if d['cake_id'] == cake_id]
        has_reviews = any(r['design_id'] in design_ids for r in MOCK_REVIEWS)
        if has_reviews:
            return jsonify({'success': False, 'message': 'Cannot delete: designs have reviews'}), 400
        
        MOCK_DESIGNS = [d for d in MOCK_DESIGNS if d['cake_id'] != cake_id]
        MOCK_CAKES = [c for c in MOCK_CAKES if c['cake_id'] != cake_id]
        save_data()  # Persist to file
        print(f"✅ Deleted cake ID {cake_id}")
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==============================================================================
# ADMIN DESIGNS CRUD
# ==============================================================================

@app.route('/admin/designs')
def admin_designs():
    """Admin designs management"""
    designs_with_details = [get_design_with_details(d) for d in MOCK_DESIGNS]
    return render_template('admin_designs.html', designs=designs_with_details, cakes=MOCK_CAKES)

@app.route('/admin/designs/add', methods=['POST'])
def admin_add_design():
    """Add new design"""
    try:
        new_id = max([d['design_id'] for d in MOCK_DESIGNS]) + 1 if MOCK_DESIGNS else 1
        
        # Handle image upload
        image_url = 'https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=800&q=80'
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"design_{new_id}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_url = url_for('static', filename=f'images/cakes/{filename}')
        
        new_design = {
            'design_id': new_id,
            'cake_id': int(request.form.get('cake_id')),
            'theme': request.form.get('theme'),
            'color_palette': request.form.get('color_palette'),
            'topper_type': request.form.get('topper_type') or None,
            'complexity_level': request.form.get('complexity_level'),
            'image_url': image_url,
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        MOCK_DESIGNS.append(new_design)
        save_data()  # Persist to file
        print(f"✅ Added design: {new_design['theme']}")
        return redirect(url_for('admin_designs') + '?success=Design added successfully!')
    except Exception as e:
        print(f"❌ Error: {e}")
        return redirect(url_for('admin_designs') + f'?error={str(e)}')

@app.route('/admin/designs/edit/<int:design_id>', methods=['POST'])
def admin_edit_design(design_id):
    """Edit design"""
    try:
        design = next((d for d in MOCK_DESIGNS if d['design_id'] == design_id), None)
        if design:
            design['cake_id'] = int(request.form.get('cake_id'))
            design['theme'] = request.form.get('theme')
            design['color_palette'] = request.form.get('color_palette')
            design['topper_type'] = request.form.get('topper_type') or None
            design['complexity_level'] = request.form.get('complexity_level')
            
            # Handle image upload
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(f"design_{design_id}_{file.filename}")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    design['image_url'] = url_for('static', filename=f'images/cakes/{filename}')
            
            save_data()  # Persist to file
            print(f"✅ Updated design ID {design_id}")
            return redirect(url_for('admin_designs') + '?success=Design updated successfully!')
        return redirect(url_for('admin_designs') + '?error=Design not found')
    except Exception as e:
        return redirect(url_for('admin_designs') + f'?error={str(e)}')

@app.route('/admin/designs/delete/<int:design_id>', methods=['POST'])
def admin_delete_design(design_id):
    """Delete design"""
    try:
        global MOCK_DESIGNS, MOCK_REVIEWS
        has_reviews = any(r['design_id'] == design_id for r in MOCK_REVIEWS)
        if has_reviews:
            return jsonify({'success': False, 'message': 'Cannot delete: design has reviews'}), 400
        
        MOCK_DESIGNS = [d for d in MOCK_DESIGNS if d['design_id'] != design_id]
        save_data()  # Persist to file
        print(f"✅ Deleted design ID {design_id}")
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==============================================================================
# ADMIN CUSTOMERS CRUD
# ==============================================================================

@app.route('/admin/customers')
def admin_customers():
    """Admin customers management"""
    customers_with_stats = [get_customer_with_stats(c) for c in MOCK_CUSTOMERS]
    return render_template('admin_customers.html', customers=customers_with_stats)

@app.route('/admin/customers/add', methods=['POST'])
def admin_add_customer():
    """Add new customer"""
    try:
        new_id = max([c['customer_id'] for c in MOCK_CUSTOMERS]) + 1 if MOCK_CUSTOMERS else 1
        new_customer = {
            'customer_id': new_id,
            'full_name': request.form.get('full_name'),
            'email': request.form.get('email'),
            'city': request.form.get('city'),
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        # Check for duplicate email
        if any(c['email'] == new_customer['email'] for c in MOCK_CUSTOMERS):
            return redirect(url_for('admin_customers') + '?error=Email already exists!')
        
        MOCK_CUSTOMERS.append(new_customer)
        save_data()  # Persist to file
        print(f"✅ Added customer: {new_customer['full_name']}")
        return redirect(url_for('admin_customers') + '?success=Customer added successfully!')
    except Exception as e:
        return redirect(url_for('admin_customers') + f'?error={str(e)}')

@app.route('/admin/customers/edit/<int:customer_id>', methods=['POST'])
def admin_edit_customer(customer_id):
    """Edit customer"""
    try:
        customer = next((c for c in MOCK_CUSTOMERS if c['customer_id'] == customer_id), None)
        if customer:
            new_email = request.form.get('email')
            # Check for duplicate email (excluding current customer)
            if any(c['email'] == new_email and c['customer_id'] != customer_id for c in MOCK_CUSTOMERS):
                return redirect(url_for('admin_customers') + '?error=Email already exists!')
            
            customer['full_name'] = request.form.get('full_name')
            customer['email'] = new_email
            customer['city'] = request.form.get('city')
            save_data()  # Persist to file
            print(f"✅ Updated customer ID {customer_id}")
            return redirect(url_for('admin_customers') + '?success=Customer updated successfully!')
        return redirect(url_for('admin_customers') + '?error=Customer not found')
    except Exception as e:
        return redirect(url_for('admin_customers') + f'?error={str(e)}')

@app.route('/admin/customers/delete/<int:customer_id>', methods=['POST'])
def admin_delete_customer(customer_id):
    """Delete customer"""
    try:
        global MOCK_CUSTOMERS, MOCK_REVIEWS
        has_reviews = any(r['customer_id'] == customer_id for r in MOCK_REVIEWS)
        if has_reviews:
            return jsonify({'success': False, 'message': 'Cannot delete: customer has reviews'}), 400
        
        MOCK_CUSTOMERS = [c for c in MOCK_CUSTOMERS if c['customer_id'] != customer_id]
        save_data()  # Persist to file
        print(f"✅ Deleted customer ID {customer_id}")
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==============================================================================
# ADMIN REVIEWS CRUD
# ==============================================================================

@app.route('/admin/reviews')
def admin_reviews():
    """Admin reviews management"""
    reviews_with_details = []
    for review in MOCK_REVIEWS:
        design = next((d for d in MOCK_DESIGNS if d['design_id'] == review['design_id']), None)
        customer = next((c for c in MOCK_CUSTOMERS if c['customer_id'] == review['customer_id']), None)
        cake = next((c for c in MOCK_CAKES if design and c['cake_id'] == design['cake_id']), None)
        reviews_with_details.append({
            **review,
            'theme': design['theme'] if design else 'Unknown',
            'cake_name': cake['cake_name'] if cake else 'Unknown',
            'customer_name': customer['full_name'] if customer else 'Unknown'
        })
    return render_template('admin_reviews.html', reviews=reviews_with_details, 
                          designs=MOCK_DESIGNS, customers=MOCK_CUSTOMERS)

@app.route('/admin/reviews/add', methods=['POST'])
def admin_add_review():
    """Add new review"""
    try:
        new_id = max([r['review_id'] for r in MOCK_REVIEWS]) + 1 if MOCK_REVIEWS else 1
        new_review = {
            'review_id': new_id,
            'customer_id': int(request.form.get('customer_id')),
            'design_id': int(request.form.get('design_id')),
            'rating': int(request.form.get('rating')),
            'review_text': request.form.get('review_text'),
            'review_date': datetime.now().strftime('%Y-%m-%d')
        }
        MOCK_REVIEWS.append(new_review)
        save_data()  # Persist to file
        print(f"✅ Added review ID {new_id}")
        return redirect(url_for('admin_reviews') + '?success=Review added successfully!')
    except Exception as e:
        return redirect(url_for('admin_reviews') + f'?error={str(e)}')

@app.route('/admin/reviews/edit/<int:review_id>', methods=['POST'])
def admin_edit_review(review_id):
    """Edit review"""
    try:
        review = next((r for r in MOCK_REVIEWS if r['review_id'] == review_id), None)
        if review:
            review['customer_id'] = int(request.form.get('customer_id'))
            review['design_id'] = int(request.form.get('design_id'))
            review['rating'] = int(request.form.get('rating'))
            review['review_text'] = request.form.get('review_text')
            save_data()  # Persist to file
            print(f"✅ Updated review ID {review_id}")
            return redirect(url_for('admin_reviews') + '?success=Review updated successfully!')
        return redirect(url_for('admin_reviews') + '?error=Review not found')
    except Exception as e:
        return redirect(url_for('admin_reviews') + f'?error={str(e)}')

@app.route('/admin/reviews/delete/<int:review_id>', methods=['POST'])
def admin_delete_review(review_id):
    """Delete review"""
    try:
        global MOCK_REVIEWS
        MOCK_REVIEWS = [r for r in MOCK_REVIEWS if r['review_id'] != review_id]
        save_data()  # Persist to file
        print(f"✅ Deleted review ID {review_id}")
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==============================================================================
# API ENDPOINTS
# ==============================================================================

@app.route('/api/cakes')
def api_cakes():
    return jsonify(MOCK_CAKES)

@app.route('/api/cakes/<int:cake_id>')
def api_cake(cake_id):
    cake = next((c for c in MOCK_CAKES if c['cake_id'] == cake_id), None)
    if cake:
        designs = [get_design_with_details(d) for d in MOCK_DESIGNS if d['cake_id'] == cake_id]
        return jsonify({**cake, 'designs': designs})
    return jsonify({'error': 'Cake not found'}), 404

@app.route('/api/designs')
def api_designs():
    return jsonify([get_design_with_details(d) for d in MOCK_DESIGNS])

@app.route('/api/designs/<int:design_id>')
def api_design(design_id):
    design = next((d for d in MOCK_DESIGNS if d['design_id'] == design_id), None)
    if design:
        return jsonify(get_design_with_details(design))
    return jsonify({'error': 'Design not found'}), 404

@app.route('/api/customers')
def api_customers():
    return jsonify([get_customer_with_stats(c) for c in MOCK_CUSTOMERS])

@app.route('/api/reviews')
def api_reviews():
    return jsonify(MOCK_REVIEWS)

# Legacy endpoints for compatibility
@app.route('/api/flavors')
def api_flavors():
    return jsonify([{'flavor_id': i+1, 'name': f, 'price_per_layer': 0} 
                    for i, f in enumerate(set(c['flavor'] for c in MOCK_CAKES))])

@app.route('/api/toppings')
def api_toppings():
    return jsonify([])

@app.route('/api/sizes')
def api_sizes():
    return jsonify([{'size_id': i+1, 'name': s, 'base_price': 0} 
                    for i, s in enumerate(set(c['size'] for c in MOCK_CAKES))])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
