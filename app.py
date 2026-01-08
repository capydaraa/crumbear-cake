# =====================================================
# CRUMBEAR CAKE MANAGEMENT SYSTEM - Production App
# Flask application with Microsoft SQL Server database
# Tables: Cakes, CakeDesigns, Customers, Reviews
# =====================================================

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from functools import wraps
import sys

# Add database directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'database'))
from db_connection import execute_query, execute_insert, get_db_connection

app = Flask(__name__, 
            template_folder='frontend/templates',
            static_folder='frontend/static')

# Configuration
app.config['UPLOAD_FOLDER'] = 'frontend/static/images/cakes'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = 'crumbear_secret_key_2024'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==============================================================================
# HELPER FUNCTIONS - Using Stored Functions and Views
# ==============================================================================

def get_design_with_details(design_id):
    """Get design with cake info and ratings using View"""
    query = """
        SELECT * FROM vw_DesignWithRatings 
        WHERE design_id = ?
    """
    results = execute_query(query, (design_id,))
    if results:
        design = results[0]
        # Calculate price using stored function
        price_query = "SELECT dbo.fn_CalculateDesignPrice(?) AS calculated_price"
        price_result = execute_query(price_query, (design_id,))
        design['calculated_price'] = price_result[0]['calculated_price'] if price_result else 0
        return design
    return None

def get_all_designs_with_details():
    """Get all designs with details using View - Featured first"""
    query = """
        SELECT 
            dr.*,
            dbo.fn_CalculateDesignPrice(dr.design_id) AS calculated_price
        FROM vw_DesignWithRatings dr
        ORDER BY dr.featured DESC, dr.design_id
    """
    return execute_query(query)

def get_customer_with_stats(customer_id):
    """Get customer with review stats using View"""
    query = """
        SELECT * FROM vw_CustomerActivity 
        WHERE customer_id = ?
    """
    results = execute_query(query, (customer_id,))
    return results[0] if results else None

# ==============================================================================
# PUBLIC ROUTES
# ==============================================================================

@app.route('/')
def index():
    """Home page - Browse cake designs with pagination"""
    try:
        # Pagination settings
        page = request.args.get('page', 1, type=int)
        per_page = 30  # 30 cakes per page
        
        # Get all designs first for total count
        all_designs = get_all_designs_with_details()
        total_designs = len(all_designs) if all_designs else 0
        total_pages = (total_designs + per_page - 1) // per_page  # Ceiling division
        
        # Calculate offset and get paginated designs
        offset = (page - 1) * per_page
        designs = all_designs[offset:offset + per_page] if all_designs else []
        
        cakes = execute_query("SELECT * FROM Cakes WHERE availability = 1")
        logged_in_customer = session.get('customer')
        
        return render_template('index.html', 
                               designs=designs, 
                               cakes=cakes, 
                               logged_in_customer=logged_in_customer,
                               page=page,
                               total_pages=total_pages,
                               total_designs=total_designs)
    except Exception as e:
        print(f"Error loading index: {e}")
        return render_template('index.html', designs=[], cakes=[], logged_in_customer=None, 
                               page=1, total_pages=1, total_designs=0, error=str(e))

@app.route('/design/<int:design_id>')
def design_detail(design_id):
    """Design detail page with reviews"""
    try:
        design = get_design_with_details(design_id)
        if not design:
            return redirect(url_for('index'))
        
        # Get cake details
        cake_query = """
            SELECT c.* FROM Cakes c
            JOIN CakeDesigns cd ON c.cake_id = cd.cake_id
            WHERE cd.design_id = ?
        """
        cake_results = execute_query(cake_query, (design_id,))
        if cake_results:
            design['frosting'] = cake_results[0]['frosting']
            design['size'] = cake_results[0]['size']
        
        # Get reviews with customer info
        reviews_query = """
            SELECT r.*, c.full_name AS customer_name, c.city
            FROM Reviews r
            JOIN Customers c ON r.customer_id = c.customer_id
            WHERE r.design_id = ?
            ORDER BY r.review_date DESC
        """
        reviews = execute_query(reviews_query, (design_id,))
        
        logged_in_customer = session.get('customer')
        return render_template('design_detail.html', 
                               design=design, 
                               reviews=reviews,
                               logged_in_customer=logged_in_customer)
    except Exception as e:
        print(f"Error loading design: {e}")
        return redirect(url_for('index'))

@app.route('/calculator')
def calculator():
    """Price calculator page"""
    try:
        cakes = execute_query("SELECT * FROM Cakes WHERE availability = 1")
        logged_in_customer = session.get('customer')
        return render_template('calculator.html', cakes=cakes, logged_in_customer=logged_in_customer)
    except Exception as e:
        return render_template('calculator.html', cakes=[], logged_in_customer=None)

# ==============================================================================
# CUSTOMER AUTHENTICATION
# ==============================================================================

@app.route('/login', methods=['GET', 'POST'])
def customer_login():
    """Customer login page"""
    next_url = request.args.get('next', '')
    success_msg = request.args.get('success', '')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        next_url = request.form.get('next', '')
        
        # Check if customer exists and password matches
        query = "SELECT * FROM Customers WHERE email = ? AND password = ?"
        results = execute_query(query, (email, password))
        
        if results:
            session['customer'] = results[0]
            if next_url:
                return redirect(next_url)
            return redirect(url_for('index'))
        return render_template('customer_auth.html', error='Invalid email or password', next_url=next_url)
    
    return render_template('customer_auth.html', next_url=next_url, success=success_msg)

@app.route('/signup', methods=['POST'])
def customer_signup():
    """Customer signup"""
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    city = request.form.get('city')
    password = request.form.get('password')
    next_url = request.form.get('next', '')
    
    try:
        # Check if email already exists
        check_query = "SELECT * FROM Customers WHERE email = ?"
        existing = execute_query(check_query, (email,))
        
        if existing:
            return render_template('customer_auth.html', error='Email already registered', next_url=next_url)
        
        # Insert new customer with password
        insert_query = """
            INSERT INTO Customers (full_name, email, city, password) 
            VALUES (?, ?, ?, ?)
        """
        execute_insert(insert_query, (full_name, email, city, password))
        
        # Redirect to login page with success message
        login_url = url_for('customer_login')
        if next_url:
            login_url += f'?next={next_url}&success=Account created! Please sign in.'
        else:
            login_url += '?success=Account created! Please sign in.'
        return redirect(login_url)
    except Exception as e:
        return render_template('customer_auth.html', error=str(e), next_url=next_url)

@app.route('/logout')
def customer_logout():
    """Customer logout"""
    session.pop('customer', None)
    return redirect(url_for('index'))

@app.route('/review/<int:design_id>', methods=['POST'])
def submit_review(design_id):
    """Submit a review for a design"""
    customer = session.get('customer')
    
    if not customer:
        return redirect(url_for('customer_login', next=url_for('design_detail', design_id=design_id)))
    
    rating = int(request.form.get('rating', 5))
    review_text = request.form.get('review_text', '')
    
    try:
        # Insert review (trigger will log to ReviewAuditLog)
        insert_query = """
            INSERT INTO Reviews (customer_id, design_id, rating, review_text)
            VALUES (?, ?, ?, ?)
        """
        execute_insert(insert_query, (customer['customer_id'], design_id, rating, review_text))
        
        return redirect(url_for('design_detail', design_id=design_id))
    except Exception as e:
        print(f"Error submitting review: {e}")
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
        
        # Check admin credentials
        query = "SELECT * FROM AdminUsers WHERE username = ?"
        results = execute_query(query, (username,))
        
        # Simple check (in production, use proper password hashing)
        if results and password == 'crumbear123':
            session['admin'] = results[0]
            return redirect(url_for('admin_dashboard'))
        return render_template('admin_login.html', error='Invalid credentials')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin', None)
    return redirect(url_for('index'))

# ==============================================================================
# ADMIN DASHBOARD - Using Stored Procedure
# ==============================================================================

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard with statistics"""
    try:
        # Use stored procedure for dashboard stats
        stats_query = "EXEC sp_GetDashboardStats"
        stats_result = execute_query(stats_query)
        stats = stats_result[0] if stats_result else {
            'total_cakes': 0, 'total_designs': 0, 'total_customers': 0,
            'total_reviews': 0, 'avg_rating': 0, 'available_cakes': 0
        }
        
        # Ensure avg_rating exists and is not None
        if stats.get('avg_rating') is None:
            stats['avg_rating'] = 0
        
        # Get top designs using stored procedure
        top_query = "EXEC sp_GetTopDesigns @top_count = 5"
        top_designs = execute_query(top_query)
        
        # Chart data using advanced queries with subqueries
        # Complexity distribution
        complexity_query = """
            SELECT complexity_level, COUNT(*) as count
            FROM CakeDesigns
            GROUP BY complexity_level
            ORDER BY 
                CASE complexity_level 
                    WHEN 'Simple' THEN 1 
                    WHEN 'Moderate' THEN 2 
                    WHEN 'Complex' THEN 3 
                    WHEN 'Expert' THEN 4 
                END
        """
        complexity_data = execute_query(complexity_query)
        
        # Rating distribution
        rating_query = """
            SELECT rating, COUNT(*) as count
            FROM Reviews
            GROUP BY rating
            ORDER BY rating
        """
        rating_data = execute_query(rating_query)
        
        # City distribution (using subquery)
        city_query = """
            SELECT city, COUNT(*) as count
            FROM Customers
            WHERE city IN (
                SELECT TOP 6 city 
                FROM Customers 
                GROUP BY city 
                ORDER BY COUNT(*) DESC
            )
            GROUP BY city
            ORDER BY count DESC
        """
        city_data = execute_query(city_query)
        
        chart_data = {
            'complexity_levels': [d['complexity_level'] for d in complexity_data] if complexity_data else [],
            'complexity_counts': [d['count'] for d in complexity_data] if complexity_data else [],
            'rating_distribution': [0, 0, 0, 0, 0],  # Initialize for 1-5 stars
            'cities': [d['city'] for d in city_data] if city_data else [],
            'city_counts': [d['count'] for d in city_data] if city_data else []
        }
        
        # Fill in rating distribution
        if rating_data:
            for d in rating_data:
                if 1 <= d['rating'] <= 5:
                    chart_data['rating_distribution'][d['rating'] - 1] = d['count']
        
        return render_template('admin_dashboard.html', 
                               stats=stats, 
                               top_designs=top_designs or [], 
                               chart_data=chart_data)
    except Exception as e:
        print(f"Dashboard error: {e}")
        # Return with empty data on error
        return render_template('admin_dashboard.html', 
                               stats={'total_cakes': 0, 'total_designs': 0, 'total_customers': 0, 
                                      'total_reviews': 0, 'avg_rating': 0, 'available_cakes': 0},
                               top_designs=[],
                               chart_data={'complexity_levels': [], 'complexity_counts': [],
                                           'rating_distribution': [0,0,0,0,0], 
                                           'cities': [], 'city_counts': []})

# ==============================================================================
# ADMIN CAKES CRUD
# ==============================================================================

@app.route('/admin/cakes')
def admin_cakes():
    """Admin cakes management using View"""
    try:
        cakes = execute_query("SELECT * FROM vw_CakeWithDesignCount ORDER BY cake_id")
        return render_template('admin_cakes.html', cakes=cakes)
    except Exception as e:
        return render_template('admin_cakes.html', cakes=[], error=str(e))

@app.route('/admin/cakes/add', methods=['POST'])
def admin_add_cake():
    """Add new cake"""
    try:
        query = """
            INSERT INTO Cakes (cake_name, flavor, frosting, size, base_price, availability)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            request.form.get('cake_name'),
            request.form.get('flavor'),
            request.form.get('frosting'),
            request.form.get('size'),
            float(request.form.get('base_price')),
            1 if request.form.get('availability') == '1' else 0
        )
        execute_insert(query, params)
        return redirect(url_for('admin_cakes') + '?success=Cake added successfully!')
    except Exception as e:
        return redirect(url_for('admin_cakes') + f'?error={str(e)}')

@app.route('/admin/cakes/edit/<int:cake_id>', methods=['POST'])
def admin_edit_cake(cake_id):
    """Edit cake (triggers trg_UpdateCakeTimestamp)"""
    try:
        query = """
            UPDATE Cakes SET
                cake_name = ?,
                flavor = ?,
                frosting = ?,
                size = ?,
                base_price = ?,
                availability = ?
            WHERE cake_id = ?
        """
        params = (
            request.form.get('cake_name'),
            request.form.get('flavor'),
            request.form.get('frosting'),
            request.form.get('size'),
            float(request.form.get('base_price')),
            1 if request.form.get('availability') == '1' else 0,
            cake_id
        )
        execute_query(query, params, fetch=False)
        return redirect(url_for('admin_cakes') + '?success=Cake updated successfully!')
    except Exception as e:
        return redirect(url_for('admin_cakes') + f'?error={str(e)}')

@app.route('/admin/cakes/delete/<int:cake_id>', methods=['POST'])
def admin_delete_cake(cake_id):
    """Delete cake (trigger prevents if has reviews)"""
    try:
        # The trigger trg_PreventCakeDeletionWithReviews will prevent deletion if designs have reviews
        execute_query("DELETE FROM Cakes WHERE cake_id = ?", (cake_id,), fetch=False)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# ==============================================================================
# ADMIN DESIGNS CRUD
# ==============================================================================

@app.route('/admin/designs')
def admin_designs():
    """Admin designs management"""
    try:
        designs = get_all_designs_with_details()
        cakes = execute_query("SELECT * FROM Cakes ORDER BY cake_name")
        return render_template('admin_designs.html', designs=designs or [], cakes=cakes or [])
    except Exception as e:
        return render_template('admin_designs.html', designs=[], cakes=[], error=str(e))

@app.route('/admin/designs/add', methods=['POST'])
def admin_add_design():
    """Add new design"""
    try:
        # Handle image upload
        image_url = 'https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=800&q=80'
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"design_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_url = url_for('static', filename=f'images/cakes/{filename}')
        
        query = """
            INSERT INTO CakeDesigns (cake_id, theme, color_palette, topper_type, complexity_level, image_url, featured)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            int(request.form.get('cake_id')),
            request.form.get('theme'),
            request.form.get('color_palette'),
            request.form.get('topper_type') or None,
            request.form.get('complexity_level'),
            image_url,
            1 if request.form.get('featured') else 0
        )
        execute_insert(query, params)
        return redirect(url_for('admin_designs') + '?success=Design added successfully!')
    except Exception as e:
        return redirect(url_for('admin_designs') + f'?error={str(e)}')

@app.route('/admin/designs/edit/<int:design_id>', methods=['POST'])
def admin_edit_design(design_id):
    """Edit design"""
    try:
        # Handle image upload
        image_update = ""
        params = [
            int(request.form.get('cake_id')),
            request.form.get('theme'),
            request.form.get('color_palette'),
            request.form.get('topper_type') or None,
            request.form.get('complexity_level'),
            1 if request.form.get('featured') else 0
        ]
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"design_{design_id}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_url = url_for('static', filename=f'images/cakes/{filename}')
                image_update = ", image_url = ?"
                params.append(image_url)
        
        params.append(design_id)
        
        query = f"""
            UPDATE CakeDesigns SET
                cake_id = ?,
                theme = ?,
                color_palette = ?,
                topper_type = ?,
                complexity_level = ?,
                featured = ?
                {image_update}
            WHERE design_id = ?
        """
        execute_query(query, tuple(params), fetch=False)
        return redirect(url_for('admin_designs') + '?success=Design updated successfully!')
    except Exception as e:
        return redirect(url_for('admin_designs') + f'?error={str(e)}')

@app.route('/admin/designs/delete/<int:design_id>', methods=['POST'])
def admin_delete_design(design_id):
    """Delete design"""
    try:
        # Check if design has reviews
        check_query = "SELECT COUNT(*) as count FROM Reviews WHERE design_id = ?"
        result = execute_query(check_query, (design_id,))
        
        if result and result[0]['count'] > 0:
            return jsonify({'success': False, 'message': 'Cannot delete: design has reviews'}), 400
        
        execute_query("DELETE FROM CakeDesigns WHERE design_id = ?", (design_id,), fetch=False)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==============================================================================
# ADMIN CUSTOMERS CRUD
# ==============================================================================

@app.route('/admin/customers')
def admin_customers():
    """Admin customers management using View"""
    try:
        customers = execute_query("SELECT * FROM vw_CustomerActivity ORDER BY customer_id")
        return render_template('admin_customers.html', customers=customers or [])
    except Exception as e:
        return render_template('admin_customers.html', customers=[], error=str(e))

@app.route('/admin/customers/add', methods=['POST'])
def admin_add_customer():
    """Add new customer (trigger validates email)"""
    try:
        query = """
            INSERT INTO Customers (full_name, email, city)
            VALUES (?, ?, ?)
        """
        params = (
            request.form.get('full_name'),
            request.form.get('email'),
            request.form.get('city')
        )
        execute_insert(query, params)
        return redirect(url_for('admin_customers') + '?success=Customer added successfully!')
    except Exception as e:
        return redirect(url_for('admin_customers') + f'?error={str(e)}')

@app.route('/admin/customers/edit/<int:customer_id>', methods=['POST'])
def admin_edit_customer(customer_id):
    """Edit customer"""
    try:
        query = """
            UPDATE Customers SET
                full_name = ?,
                email = ?,
                city = ?
            WHERE customer_id = ?
        """
        params = (
            request.form.get('full_name'),
            request.form.get('email'),
            request.form.get('city'),
            customer_id
        )
        execute_query(query, tuple(params), fetch=False)
        return redirect(url_for('admin_customers') + '?success=Customer updated successfully!')
    except Exception as e:
        return redirect(url_for('admin_customers') + f'?error={str(e)}')

@app.route('/admin/customers/delete/<int:customer_id>', methods=['POST'])
def admin_delete_customer(customer_id):
    """Delete customer"""
    try:
        # Check if customer has reviews using function
        check_query = "SELECT dbo.fn_GetCustomerReviewCount(?) as count"
        result = execute_query(check_query, (customer_id,))
        
        if result and result[0]['count'] > 0:
            return jsonify({'success': False, 'message': 'Cannot delete: customer has reviews'}), 400
        
        execute_query("DELETE FROM Customers WHERE customer_id = ?", (customer_id,), fetch=False)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==============================================================================
# ADMIN REVIEWS CRUD
# ==============================================================================

@app.route('/admin/reviews')
def admin_reviews():
    """Admin reviews management"""
    try:
        # First ensure the is_hidden column exists
        try:
            execute_query("""
                IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('Reviews') AND name = 'is_hidden')
                BEGIN
                    ALTER TABLE Reviews ADD is_hidden BIT DEFAULT 0
                END
            """, fetch=False)
        except:
            pass  # Column might already exist
        
        # Complex query with subquery
        query = """
            SELECT 
                r.*,
                ISNULL(r.is_hidden, 0) AS is_hidden,
                c.full_name AS customer_name,
                cd.theme,
                ck.cake_name,
                (SELECT AVG(CAST(r2.rating AS DECIMAL(3,2))) 
                 FROM Reviews r2 
                 WHERE r2.design_id = r.design_id) AS design_avg_rating
            FROM Reviews r
            JOIN Customers c ON r.customer_id = c.customer_id
            JOIN CakeDesigns cd ON r.design_id = cd.design_id
            JOIN Cakes ck ON cd.cake_id = ck.cake_id
            ORDER BY r.review_date DESC
        """
        reviews = execute_query(query)
        designs = execute_query("SELECT design_id, theme FROM CakeDesigns")
        customers = execute_query("SELECT customer_id, full_name FROM Customers")
        return render_template('admin_reviews.html', 
                               reviews=reviews or [], 
                               designs=designs or [], 
                               customers=customers or [])
    except Exception as e:
        return render_template('admin_reviews.html', reviews=[], designs=[], customers=[], error=str(e))

@app.route('/admin/reviews/add', methods=['POST'])
def admin_add_review():
    """Add new review (trigger logs to audit)"""
    try:
        query = """
            INSERT INTO Reviews (customer_id, design_id, rating, review_text)
            VALUES (?, ?, ?, ?)
        """
        params = (
            int(request.form.get('customer_id')),
            int(request.form.get('design_id')),
            int(request.form.get('rating')),
            request.form.get('review_text')
        )
        execute_insert(query, params)
        return redirect(url_for('admin_reviews') + '?success=Review added successfully!')
    except Exception as e:
        return redirect(url_for('admin_reviews') + f'?error={str(e)}')

@app.route('/admin/reviews/edit/<int:review_id>', methods=['POST'])
def admin_edit_review(review_id):
    """Edit review"""
    try:
        query = """
            UPDATE Reviews SET
                customer_id = ?,
                design_id = ?,
                rating = ?,
                review_text = ?
            WHERE review_id = ?
        """
        params = (
            int(request.form.get('customer_id')),
            int(request.form.get('design_id')),
            int(request.form.get('rating')),
            request.form.get('review_text'),
            review_id
        )
        execute_query(query, tuple(params), fetch=False)
        return redirect(url_for('admin_reviews') + '?success=Review updated successfully!')
    except Exception as e:
        return redirect(url_for('admin_reviews') + f'?error={str(e)}')

@app.route('/admin/reviews/delete/<int:review_id>', methods=['POST'])
def admin_delete_review(review_id):
    """Delete review"""
    try:
        execute_query("DELETE FROM Reviews WHERE review_id = ?", (review_id,), fetch=False)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/reviews/toggle-hide/<int:review_id>', methods=['POST'])
def admin_toggle_hide_review(review_id):
    """Toggle review visibility (hide/show)"""
    try:
        data = request.get_json()
        is_hidden = 1 if data.get('is_hidden', False) else 0
        
        # First ensure the is_hidden column exists
        try:
            execute_query("""
                IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('Reviews') AND name = 'is_hidden')
                BEGIN
                    ALTER TABLE Reviews ADD is_hidden BIT DEFAULT 0
                END
            """, fetch=False)
        except:
            pass  # Column might already exist
        
        execute_query("UPDATE Reviews SET is_hidden = ? WHERE review_id = ?", (is_hidden, review_id), fetch=False)
        return jsonify({'success': True, 'is_hidden': bool(is_hidden)})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==============================================================================
# API ENDPOINTS - For external access
# ==============================================================================

@app.route('/api/cakes')
def api_cakes():
    """API: Get all cakes"""
    try:
        cakes = execute_query("SELECT * FROM vw_CakeWithDesignCount")
        return jsonify(cakes or [])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cakes/<int:cake_id>')
def api_cake(cake_id):
    """API: Get cake with designs using stored procedure"""
    try:
        cake = execute_query("SELECT * FROM Cakes WHERE cake_id = ?", (cake_id,))
        if not cake:
            return jsonify({'error': 'Cake not found'}), 404
        
        # Use stored procedure to get designs
        designs = execute_query("EXEC sp_GetCakeDesigns @cake_id = ?", (cake_id,))
        
        result = cake[0]
        result['designs'] = designs or []
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/designs')
def api_designs():
    """API: Get all designs with details"""
    try:
        designs = get_all_designs_with_details()
        return jsonify(designs or [])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/designs/<int:design_id>')
def api_design(design_id):
    """API: Get design details"""
    try:
        design = get_design_with_details(design_id)
        if not design:
            return jsonify({'error': 'Design not found'}), 404
        return jsonify(design)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers')
def api_customers():
    """API: Get all customers with stats"""
    try:
        customers = execute_query("SELECT * FROM vw_CustomerActivity")
        return jsonify(customers or [])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reviews')
def api_reviews():
    """API: Get all reviews"""
    try:
        reviews = execute_query("SELECT * FROM Reviews ORDER BY review_date DESC")
        return jsonify(reviews or [])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customer/<int:customer_id>/reviews')
def api_customer_reviews(customer_id):
    """API: Get customer reviews using stored procedure"""
    try:
        reviews = execute_query("EXEC sp_GetCustomerReviews @customer_id = ?", (customer_id,))
        return jsonify(reviews or [])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/cakes')
def api_search_cakes():
    """API: Search cakes using stored procedure"""
    try:
        search_term = request.args.get('q')
        flavor = request.args.get('flavor')
        size = request.args.get('size')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        
        query = """
            EXEC sp_SearchCakes 
                @search_term = ?,
                @flavor = ?,
                @size = ?,
                @min_price = ?,
                @max_price = ?
        """
        params = (
            search_term or None,
            flavor or None,
            size or None,
            float(min_price) if min_price else None,
            float(max_price) if max_price else None
        )
        results = execute_query(query, params)
        return jsonify(results or [])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/top-designs')
def api_top_designs():
    """API: Get top rated designs using stored procedure"""
    try:
        count = request.args.get('count', 10, type=int)
        designs = execute_query("EXEC sp_GetTopDesigns @top_count = ?", (count,))
        return jsonify(designs or [])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/stats')
def api_dashboard_stats():
    """API: Get dashboard statistics using stored procedure"""
    try:
        stats = execute_query("EXEC sp_GetDashboardStats")
        return jsonify(stats[0] if stats else {})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Legacy endpoints for compatibility
@app.route('/api/flavors')
def api_flavors():
    """API: Get flavors for calculator"""
    # Return fixed calculator flavors
    flavors = [
        {'flavor_id': 1, 'name': 'Chocolate', 'price_per_layer': 30},
        {'flavor_id': 2, 'name': 'Vanilla', 'price_per_layer': 40},
        {'flavor_id': 3, 'name': 'Strawberry', 'price_per_layer': 55},
        {'flavor_id': 4, 'name': 'Ube', 'price_per_layer': 45},
        {'flavor_id': 5, 'name': 'Mocha', 'price_per_layer': 35}
    ]
    return jsonify(flavors)

@app.route('/api/sizes')
def api_sizes():
    """API: Get sizes for calculator"""
    # Return fixed calculator sizes
    sizes = [
        {'size_id': 1, 'name': '4x3', 'description': '4 inches diameter, 3 inches height', 'base_price': 200},
        {'size_id': 2, 'name': '5x3', 'description': '5 inches diameter, 3 inches height', 'base_price': 300},
        {'size_id': 3, 'name': '6x3', 'description': '6 inches diameter, 3 inches height', 'base_price': 400}
    ]
    return jsonify(sizes)

# ==============================================================================
# ERROR HANDLERS
# ==============================================================================

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html', designs=[], cakes=[], logged_in_customer=None), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html', designs=[], cakes=[], logged_in_customer=None, error='Internal server error'), 500

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("CRUMBEAR CAKE MANAGEMENT SYSTEM - Production Mode")
    print("=" * 60)
    print("Using Microsoft SQL Server Database")
    print("Make sure SQL Server is running (docker-compose up -d)")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5001)
