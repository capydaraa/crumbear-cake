# Crumbear Cake Management System

## Project Overview
A web-based cake browsing and price calculator system that allows customers to view pre-made cakes and calculate customized cake prices. Includes an admin panel for managing cakes, toppings, colors, and viewing analytics.

**Date Created:** November 27, 2025  
**Database:** Microsoft SQL Server 2019+ (via Docker)  
**Framework:** Python Flask (Backend API) + HTML/CSS/Bootstrap (Frontend)

---

## 🎯 Project Requirements Checklist

### Core Requirements
- [x] Individual unique system design
- [ ] CRUD operations for 4+ related tables
- [ ] Sample data: 1,000-2,000 records per table
- [ ] API-based communication between GUI and database
- [ ] User-friendly GUI with validation and error handling
- [ ] Dashboard with data visualization

### Advanced SQL Features (All Required)
- [ ] **Trigger** - Auto-update cake view count when browsed
- [ ] **Stored Function** - Calculate total price for customized cake
- [ ] **Stored Procedure** - Generate price estimate report
- [ ] **View** - Popular cakes view (most viewed)
- [ ] **Index** - On cake names, categories, and prices for fast searching
- [ ] **Subquery** - Find cakes with above-average base prices

---

## 🏗️ System Architecture

### Tech Stack
- **Database:** Microsoft SQL Server 2019+ (Docker container)
- **Backend API:** Python Flask + pyodbc/pymssql
- **Frontend:** HTML5 + CSS3 + Bootstrap 5 + JavaScript
- **Charts/Visualization:** Chart.js
- **Environment:** Local development (macOS)

### Application Structure
```
ADS/
├── DOCS                          # Project requirements
├── PROJECT_PLAN.md              # This file
├── database/
│   ├── schema.sql               # Database schema creation
│   ├── seed_data.sql            # Sample data insertion (1000-2000 records)
│   ├── triggers.sql             # Trigger implementations
│   ├── functions.sql            # Stored functions
│   ├── procedures.sql           # Stored procedures
│   ├── views.sql                # View definitions
│   └── indexes.sql              # Index creation
├── backend/
│   ├── app.py                   # Flask application entry point
│   ├── config.py                # Database configuration
│   ├── requirements.txt         # Python dependencies
│   ├── api/
│   │   ├── __init__.py
│   │   ├── cakes.py            # Cake CRUD endpoints
│   │   ├── toppings.py         # Topping CRUD endpoints
│   │   ├── colors.py           # Color CRUD endpoints
│   │   ├── flavors.py          # Flavor CRUD endpoints
│   │   ├── calculator.py       # Price calculation endpoint
│   │   └── analytics.py        # Dashboard data endpoints
│   └── models/
│       └── database.py          # Database connection handler
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   └── calculator.js
│   │   └── images/
│   │       └── cakes/           # Cake images
│   └── templates/
│       ├── base.html            # Base template
│       ├── index.html           # Home/Browse cakes
│       ├── calculator.html      # Price calculator
│       ├── admin_login.html     # Admin authentication
│       ├── admin_dashboard.html # Admin analytics dashboard
│       ├── admin_cakes.html     # Manage cakes (CRUD)
│       ├── admin_toppings.html  # Manage toppings (CRUD)
│       ├── admin_colors.html    # Manage colors (CRUD)
│       └── admin_flavors.html   # Manage flavors (CRUD)
└── docker-compose.yml           # SQL Server Docker setup
```

---

## 📊 Database Design

### Tables (Minimum 4 Required)

#### 1. **Cakes** (Main catalog)
```sql
- cake_id (PK, INT, IDENTITY)
- name (VARCHAR(100), NOT NULL)
- description (TEXT)
- category (VARCHAR(50)) -- Birthday, Wedding, Anniversaries, Cartoons
- image_url (VARCHAR(255))
- base_price_4x3 (DECIMAL(10,2))
- base_price_5x3 (DECIMAL(10,2))
- base_price_6x3 (DECIMAL(10,2))
- is_featured (BIT, DEFAULT 0)
- view_count (INT, DEFAULT 0)
- created_at (DATETIME, DEFAULT GETDATE())
- updated_at (DATETIME, DEFAULT GETDATE())
```

#### 2. **Toppings** (Cake toppings)
```sql
- topping_id (PK, INT, IDENTITY)
- name (VARCHAR(100), NOT NULL)
- price (DECIMAL(10,2), NOT NULL)
- is_available (BIT, DEFAULT 1)
- image_url (VARCHAR(255))
- created_at (DATETIME, DEFAULT GETDATE())
```

#### 3. **IcingColors** (Color options for 3 parts)
```sql
- color_id (PK, INT, IDENTITY)
- color_name (VARCHAR(50), NOT NULL) -- e.g., "Red", "Blue", "Pink"
- hex_code (VARCHAR(7)) -- e.g., "#FF0000"
- shade (VARCHAR(20)) -- Light, Medium, Dark
- price_multiplier (DECIMAL(5,2)) -- e.g., 1.0 (light), 1.5 (medium), 2.0 (dark)
- is_available (BIT, DEFAULT 1)
- created_at (DATETIME, DEFAULT GETDATE())
```

#### 4. **Flavors** (Cake flavors)
```sql
- flavor_id (PK, INT, IDENTITY)
- name (VARCHAR(100), NOT NULL) -- e.g., Chocolate, Vanilla, Red Velvet
- price_per_layer (DECIMAL(10,2), NOT NULL)
- is_available (BIT, DEFAULT 1)
- created_at (DATETIME, DEFAULT GETDATE())
```

#### 5. **PriceEstimates** (Track customer calculations)
```sql
- estimate_id (PK, INT, IDENTITY)
- cake_id (FK to Cakes, NULL if custom)
- size (VARCHAR(10)) -- "4x3", "5x3", "6x3"
- num_layers (INT)
- flavor_id (FK to Flavors)
- has_message (BIT)
- is_rush (BIT)
- total_price (DECIMAL(10,2))
- estimate_date (DATETIME, DEFAULT GETDATE())
```

#### 6. **EstimateToppings** (Junction table)
```sql
- estimate_topping_id (PK, INT, IDENTITY)
- estimate_id (FK to PriceEstimates)
- topping_id (FK to Toppings)
- quantity (INT)
```

#### 7. **EstimateIcing** (Junction table for icing parts)
```sql
- estimate_icing_id (PK, INT, IDENTITY)
- estimate_id (FK to PriceEstimates)
- icing_part (VARCHAR(20)) -- "Base", "Sides", "Other"
- color_id (FK to IcingColors)
```

#### 8. **AdminUsers** (Simple admin authentication)
```sql
- admin_id (PK, INT, IDENTITY)
- username (VARCHAR(50), UNIQUE, NOT NULL)
- password_hash (VARCHAR(255), NOT NULL)
- created_at (DATETIME, DEFAULT GETDATE())
```

### Relationships
- **Cakes** ↔ **PriceEstimates** (One-to-Many, optional)
- **Flavors** ↔ **PriceEstimates** (One-to-Many)
- **PriceEstimates** ↔ **EstimateToppings** (One-to-Many)
- **Toppings** ↔ **EstimateToppings** (One-to-Many)
- **PriceEstimates** ↔ **EstimateIcing** (One-to-Many)
- **IcingColors** ↔ **EstimateIcing** (One-to-Many)

---

## 🔧 Advanced SQL Features Implementation

### 1. Trigger: Auto-Update View Count
```sql
-- When a cake is viewed (estimate created), increment view_count
CREATE TRIGGER trg_UpdateCakeViewCount
ON PriceEstimates
AFTER INSERT
AS
BEGIN
    UPDATE Cakes
    SET view_count = view_count + 1
    WHERE cake_id IN (SELECT cake_id FROM inserted WHERE cake_id IS NOT NULL)
END
```

### 2. Stored Function: Calculate Total Price
```sql
-- Calculate customized cake total price
CREATE FUNCTION fn_CalculateCustomCakePrice(
    @base_price DECIMAL(10,2),
    @num_layers INT,
    @flavor_price_per_layer DECIMAL(10,2),
    @topping_total DECIMAL(10,2),
    @icing_total DECIMAL(10,2),
    @has_message BIT,
    @is_rush BIT
)
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @total DECIMAL(10,2)
    DECLARE @message_fee DECIMAL(10,2) = 50.00
    DECLARE @rush_multiplier DECIMAL(5,2) = 1.5
    
    SET @total = @base_price + 
                 (@num_layers * @flavor_price_per_layer) + 
                 @topping_total + 
                 @icing_total
    
    IF @has_message = 1
        SET @total = @total + @message_fee
    
    IF @is_rush = 1
        SET @total = @total * @rush_multiplier
    
    RETURN @total
END
```

### 3. Stored Procedure: Generate Price Report
```sql
-- Get price estimate statistics
CREATE PROCEDURE sp_GetPriceEstimateReport
    @start_date DATETIME,
    @end_date DATETIME
AS
BEGIN
    SELECT 
        COUNT(*) as total_estimates,
        AVG(total_price) as avg_price,
        MIN(total_price) as min_price,
        MAX(total_price) as max_price,
        SUM(CASE WHEN is_rush = 1 THEN 1 ELSE 0 END) as rush_orders
    FROM PriceEstimates
    WHERE estimate_date BETWEEN @start_date AND @end_date
END
```

### 4. View: Popular Cakes
```sql
-- View most viewed cakes
CREATE VIEW vw_PopularCakes AS
SELECT TOP 10
    cake_id,
    name,
    category,
    view_count,
    base_price_4x3,
    image_url
FROM Cakes
WHERE view_count > 0
ORDER BY view_count DESC
```

### 5. Indexes
```sql
-- Fast searching by name and category
CREATE INDEX idx_cake_name ON Cakes(name)
CREATE INDEX idx_cake_category ON Cakes(category)
CREATE INDEX idx_cake_price ON Cakes(base_price_4x3)
CREATE INDEX idx_estimate_date ON PriceEstimates(estimate_date)
```

### 6. Subquery Example
```sql
-- Find cakes with above-average base prices
SELECT cake_id, name, base_price_4x3
FROM Cakes
WHERE base_price_4x3 > (
    SELECT AVG(base_price_4x3)
    FROM Cakes
)
ORDER BY base_price_4x3 DESC
```

---

## 🎨 Features

### Customer-Facing Features
1. **Browse Cakes**
   - View all cakes by category (Birthday, Wedding, Anniversaries, Cartoons)
   - Filter by category and price range
   - View cake details (images, sizes, base prices)
   - Responsive grid layout

2. **Price Calculator**
   - Select base cake or start from scratch
   - Choose size: 4x3, 5x3, 6x3
   - Select number of layers (1-5)
   - Choose flavor (affects price per layer)
   - Add toppings with quantities
   - Select icing colors for 3 parts (Base, Sides, Other):
     - 10 color options
     - Each with 3 shades (Light, Medium, Dark)
   - Add message on cake (+₱50)
   - Rush order (1.5x multiplier)
   - Real-time price calculation
   - Save estimate to database

### Admin Features
1. **Authentication**
   - Simple login system
   - Session management

2. **Dashboard** (Analytics)
   - Most viewed cakes (chart)
   - Price estimate trends over time (line chart)
   - Total estimates count
   - Average/Min/Max prices
   - Rush order percentage

3. **Manage Cakes** (CRUD)
   - Add new cake (with image upload)
   - Edit existing cakes
   - Delete cakes (with confirmation)
   - View all cakes in table format
   - Toggle featured status

4. **Manage Toppings** (CRUD)
   - Add/Edit/Delete toppings
   - Set availability status
   - Update prices

5. **Manage Colors** (CRUD)
   - Add/Edit/Delete colors with shades
   - Set price multipliers
   - Manage availability

6. **Manage Flavors** (CRUD)
   - Add/Edit/Delete flavors
   - Set price per layer
   - Manage availability

---

## 🚀 Implementation Plan

### Phase 1: Setup (Day 1)
- [ ] Set up SQL Server via Docker
- [ ] Create database and schema
- [ ] Set up Python virtual environment
- [ ] Install Flask and dependencies
- [ ] Create project folder structure

### Phase 2: Database (Day 2-3)
- [ ] Create all tables with relationships
- [ ] Implement triggers
- [ ] Create stored functions
- [ ] Create stored procedures
- [ ] Create views
- [ ] Add indexes
- [ ] Generate seed data (1000-2000 records per table)

### Phase 3: Backend API (Day 4-5)
- [ ] Set up Flask application structure
- [ ] Implement database connection
- [ ] Create API endpoints for Cakes CRUD
- [ ] Create API endpoints for Toppings CRUD
- [ ] Create API endpoints for Colors CRUD
- [ ] Create API endpoints for Flavors CRUD
- [ ] Create price calculator endpoint (use stored function)
- [ ] Create analytics endpoints
- [ ] Add error handling and validation

### Phase 4: Frontend - Customer (Day 6-7)
- [ ] Create base template with Bootstrap
- [ ] Build home page (browse cakes)
- [ ] Build cake detail page
- [ ] Build price calculator interface
- [ ] Implement real-time price calculation
- [ ] Add form validations
- [ ] Add confirmation messages

### Phase 5: Frontend - Admin (Day 8-9)
- [ ] Create admin login page
- [ ] Build admin dashboard with charts
- [ ] Build CRUD interface for Cakes
- [ ] Build CRUD interface for Toppings
- [ ] Build CRUD interface for Colors
- [ ] Build CRUD interface for Flavors
- [ ] Add delete confirmations
- [ ] Add success/error notifications

### Phase 6: Testing & Polish (Day 10)
- [ ] Test all CRUD operations
- [ ] Test price calculator accuracy
- [ ] Test advanced SQL features
- [ ] Verify sample data performance
- [ ] Test responsive design
- [ ] Fix bugs
- [ ] Add loading states
- [ ] Optimize queries

### Phase 7: Documentation (Day 11)
- [ ] Document API endpoints
- [ ] Document database schema
- [ ] Create setup instructions
- [ ] Add code comments
- [ ] Prepare presentation

---

## 📋 Sample Data Requirements

Each table needs 1,000-2,000 records:

1. **Cakes**: 1,500 records
   - 375 Birthday cakes
   - 375 Wedding cakes
   - 375 Anniversary cakes
   - 375 Cartoon cakes

2. **Toppings**: 1,000 records
   - Generate variations with different prices

3. **IcingColors**: 1,200 records
   - 10 base colors × 3 shades × 40 variations

4. **Flavors**: 1,000 records
   - Common flavors with price variations

5. **PriceEstimates**: 2,000 records
   - Realistic customer estimate history

---

## 🎨 Color Scheme & Branding

**Crumbear Brand Colors** (Suggested):
- Primary: Soft Pink (#FFB6C1)
- Secondary: Cream (#FFF8DC)
- Accent: Brown (#8B4513)
- Text: Dark Brown (#3E2723)

---

## 📦 Python Dependencies

```txt
Flask==3.0.0
flask-cors==4.0.0
pyodbc==5.0.1
python-dotenv==1.0.0
werkzeug==3.0.1
```

---

## 🐳 Docker Setup

SQL Server 2019 container configuration:
- Port: 1433
- SA Password: (to be set)
- Database: CrumbearDB

---

## 🔐 Security Considerations

- Admin password hashing (bcrypt)
- SQL injection prevention (parameterized queries)
- Input validation on all forms
- File upload restrictions (images only)
- Session timeout for admin

---

## 📊 Price Calculator Logic

### Base Calculation:
```
Total Price = Base Price (size) 
            + (Layers × Flavor Price per Layer)
            + (Σ Topping Prices × Quantities)
            + (Σ Icing Color Multipliers)
            + (Message Fee: ₱50 if selected)
            × (Rush Multiplier: 1.5 if selected)
```

### Icing Pricing:
- Light shade: 1.0x multiplier
- Medium shade: 1.5x multiplier  
- Dark shade: 2.0x multiplier
- Applied to 3 parts: Base, Sides, Other

---

## 🎯 Success Criteria

- [ ] All 4+ tables with proper relationships
- [ ] 1,000-2,000 records per table
- [ ] All 6 advanced SQL features working
- [ ] Full CRUD operations via GUI
- [ ] Price calculator with real-time updates
- [ ] Admin dashboard with 2+ visualizations
- [ ] Responsive web design
- [ ] Input validation and error handling
- [ ] API-based architecture
- [ ] Clean, documented code

---

## 📝 Notes

- System is for browsing and price estimation only (no actual ordering/payment)
- Focus on demonstrating database concepts and GUI integration
- Performance testing with large dataset to show indexing benefits
- All SQL scripts must be executable and well-documented

---

**Last Updated:** November 27, 2025
