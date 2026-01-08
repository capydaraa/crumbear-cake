# 🧸 Crumbear Cake Management System

A full-stack web application for managing a custom cake shop, built with **Flask** and **Microsoft SQL Server 2019**.

---

## 📋 Project Features

### Database (4 Related Tables)
- **Cakes** - Base cake products with flavor, frosting, size, price
- **CakeDesigns** - Design variations linked to cakes (themes, colors, toppers)
- **Customers** - Customer profiles for reviews
- **Reviews** - Customer reviews with ratings

### Advanced SQL Features
- ✅ **4 Views** - Pre-built queries for common data access patterns
- ✅ **4 Triggers** - Automatic timestamp updates, audit logging, validation
- ✅ **4 Scalar Functions** - Price calculations, review counts
- ✅ **5 Stored Procedures** - Dashboard stats, search, CRUD operations
- ✅ **12 Indexes** - Performance optimization
- ✅ **Subqueries** - Used throughout for complex data retrieval

### GUI Features
- ✅ **Public Pages** - Homepage, design catalog, design details
- ✅ **Admin Dashboard** - Statistics with Chart.js visualizations
- ✅ **CRUD Operations** - Full Create, Read, Update, Delete for all tables
- ✅ **Form Validation** - Client and server-side validation
- ✅ **Responsive Design** - Bootstrap 5, works on all devices
- ✅ **Notifications** - Success/error alerts for all actions

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker Desktop (for SQL Server)
- ODBC Driver 18 for SQL Server

### 1. Clone and Install Dependencies

```bash
cd /Users/bubby/Desktop/ADS
pip3 install -r requirements.txt
```

### 2. Start SQL Server (Docker)

```bash
# Start the SQL Server container
docker-compose up -d

# Wait ~30 seconds for SQL Server to initialize
```

### 3. Initialize the Database

```bash
# Create database and schema
python3 scripts/init_db.py

# Verify database structure
python3 scripts/init_db.py --verify
```

### 4. Run the Application

**Production Mode (SQL Server):**
```bash
python3 app.py
```

**Preview Mode (JSON Mock Data):**
```bash
python3 preview_app.py
```

### 5. Access the Application

- **Homepage:** http://localhost:5001
- **Admin Panel:** http://localhost:5001/admin/login
  - Username: `admin`
  - Password: `crumbear123`

---

## 📂 Project Structure

```
ADS/
├── app.py                      # Production Flask app (SQL Server)
├── preview_app.py              # Preview app (JSON mock data)
├── docker-compose.yml          # SQL Server container config
├── requirements.txt            # Python dependencies
│
├── database/
│   ├── db_connection.py        # pyodbc connection module
│   ├── schema.sql              # Complete database schema
│   └── seed_data.sql           # Seed data (1000-2000 records)
│
├── frontend/
│   ├── static/
│   │   ├── css/style.css       # Custom styles (pastel pink theme)
│   │   ├── js/
│   │   │   ├── main.js         # General JavaScript
│   │   │   └── calculator.js   # Price calculator logic
│   │   └── images/
│   │       ├── logo-main.png   # Crumbear logo
│   │       └── cakes/          # Uploaded cake images
│   │
│   └── templates/
│       ├── base.html           # Base template
│       ├── index.html          # Homepage (design catalog)
│       ├── design_detail.html  # Individual design page
│       ├── calculator.html     # Price calculator
│       ├── customer_auth.html  # Customer login/signup
│       ├── admin_base.html     # Admin base template
│       ├── admin_login.html    # Admin login
│       ├── admin_dashboard.html # Dashboard with charts
│       ├── admin_cakes.html    # Manage cakes
│       ├── admin_designs.html  # Manage designs
│       ├── admin_customers.html # Manage customers
│       └── admin_reviews.html  # Manage reviews
│
├── scripts/
│   ├── init_db.py              # Database initialization
│   └── check_images.py         # Image validation utility
│
└── data/
    └── crumbear_data.json      # Mock data for preview mode
```

---

## 🗄️ Database Schema

### Tables

```sql
Cakes (cake_id, cake_name, flavor, frosting, size, base_price, availability)
CakeDesigns (design_id, cake_id, theme, color_palette, topper_type, complexity_level, image_url)
Customers (customer_id, full_name, email, city, join_date)
Reviews (review_id, customer_id, design_id, rating, review_text, review_date)
AdminUsers (admin_id, username, password_hash, email, full_name)
ReviewAuditLog (log_id, review_id, action, changed_by, change_date)
```

### Views
- `vw_CakeWithDesignCount` - Cakes with their design counts
- `vw_DesignWithRatings` - Designs with average ratings
- `vw_CustomerActivity` - Customers with review statistics
- `vw_TopRatedDesigns` - Top 10 designs by rating

### Stored Procedures
- `sp_GetDashboardStats` - Dashboard statistics
- `sp_GetTopDesigns` - Top rated designs
- `sp_SearchCakes` - Advanced cake search
- `sp_GetCakeDesigns` - Designs for a specific cake
- `sp_GetCustomerReviews` - Customer's review history

### Functions
- `fn_CalculateDesignPrice` - Calculate design price with complexity multiplier
- `fn_GetDesignAverageRating` - Get average rating for a design
- `fn_GetCustomerReviewCount` - Count customer's reviews
- `fn_ValidateEmail` - Email format validation

### Triggers
- `trg_UpdateCakeTimestamp` - Auto-update timestamps on cake changes
- `trg_ValidateCustomerEmail` - Validate email format on insert
- `trg_LogReviewChanges` - Audit trail for review modifications
- `trg_PreventCakeDeletionWithReviews` - Prevent deleting cakes with reviews

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/cakes` | GET | Get all cakes |
| `/api/cakes/<id>` | GET | Get cake with designs |
| `/api/designs` | GET | Get all designs |
| `/api/designs/<id>` | GET | Get design details |
| `/api/customers` | GET | Get all customers |
| `/api/reviews` | GET | Get all reviews |
| `/api/search/cakes` | GET | Search cakes (with filters) |
| `/api/top-designs` | GET | Get top rated designs |
| `/api/dashboard/stats` | GET | Get dashboard statistics |

---

## 🔧 Configuration

### Environment Variables (Optional)

```bash
export DB_SERVER="localhost,1433"
export DB_NAME="CrumbearDB"
export DB_USER="sa"
export DB_PASSWORD="Crumbear2025!"
export DB_DRIVER="{ODBC Driver 18 for SQL Server}"
```

### Docker Configuration

The SQL Server container is configured in `docker-compose.yml`:
- **Image:** mcr.microsoft.com/mssql/server:2019-latest
- **Port:** 1433
- **Password:** Crumbear2025!

---

## 📊 Admin Dashboard

The admin dashboard includes:
- Total counts for cakes, designs, customers, reviews
- Average rating across all reviews
- **Chart 1:** Complexity level distribution (Doughnut)
- **Chart 2:** Rating distribution (Bar)
- **Chart 3:** Customer distribution by city (Bar)
- Top 5 highest-rated designs

---

## 🎨 UI Theme

- **Primary Color:** Pastel Pink (#FFB4B4)
- **Secondary Color:** Soft Red (#C85C5C)
- **Font:** Poppins (Google Fonts)
- **Framework:** Bootstrap 5.3
- **Charts:** Chart.js 4.4.0

---

## 📝 Notes

- The preview app (`preview_app.py`) uses JSON file storage for testing without a database
- The production app (`app.py`) requires SQL Server to be running
- Default admin credentials: `admin` / `crumbear123`
- Default customer password for testing: `password123`
