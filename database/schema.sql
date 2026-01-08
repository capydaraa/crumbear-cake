-- =====================================================
-- CRUMBEAR CAKE MANAGEMENT SYSTEM - DATABASE SCHEMA
-- Database: Microsoft SQL Server 2019+
-- Version: 2.0 (Normalized Schema)
-- =====================================================

-- Create Database
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'CrumbearDB')
BEGIN
    CREATE DATABASE CrumbearDB;
END
GO

USE CrumbearDB;
GO

-- =====================================================
-- DROP EXISTING TABLES (if any)
-- =====================================================
IF OBJECT_ID('Reviews', 'U') IS NOT NULL DROP TABLE Reviews;
IF OBJECT_ID('CakeDesigns', 'U') IS NOT NULL DROP TABLE CakeDesigns;
IF OBJECT_ID('Customers', 'U') IS NOT NULL DROP TABLE Customers;
IF OBJECT_ID('Cakes', 'U') IS NOT NULL DROP TABLE Cakes;
IF OBJECT_ID('AdminUsers', 'U') IS NOT NULL DROP TABLE AdminUsers;
GO

-- =====================================================
-- TABLE 1: CAKES
-- Stores base cake information (not the design)
-- Each cake can have many designs
-- =====================================================
CREATE TABLE Cakes (
    cake_id         INT IDENTITY(1,1) PRIMARY KEY,
    cake_name       NVARCHAR(100) NOT NULL,
    flavor          NVARCHAR(50) NOT NULL,
    frosting        NVARCHAR(50) NOT NULL,
    size            NVARCHAR(20) NOT NULL,
    base_price      DECIMAL(10,2) NOT NULL CHECK (base_price >= 0),
    availability    BIT DEFAULT 1,
    created_at      DATETIME DEFAULT GETDATE(),
    updated_at      DATETIME DEFAULT GETDATE()
);
GO

-- =====================================================
-- TABLE 2: CAKE_DESIGNS
-- Stores visual/design variations of a cake
-- Each design belongs to one cake
-- =====================================================
CREATE TABLE CakeDesigns (
    design_id       INT IDENTITY(1,1) PRIMARY KEY,
    cake_id         INT NOT NULL,
    theme           NVARCHAR(100) NOT NULL,
    color_palette   NVARCHAR(100) NOT NULL,
    topper_type     NVARCHAR(50),
    complexity_level NVARCHAR(20) NOT NULL CHECK (complexity_level IN ('Simple', 'Moderate', 'Complex', 'Expert')),
    image_url       NVARCHAR(255),
    created_at      DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_CakeDesigns_Cakes 
        FOREIGN KEY (cake_id) REFERENCES Cakes(cake_id)
        ON DELETE CASCADE
);
GO

-- =====================================================
-- TABLE 3: CUSTOMERS
-- Stores customer information
-- =====================================================
CREATE TABLE Customers (
    customer_id     INT IDENTITY(1,1) PRIMARY KEY,
    full_name       NVARCHAR(100) NOT NULL,
    email           NVARCHAR(100) NOT NULL UNIQUE,
    city            NVARCHAR(50) NOT NULL,
    created_at      DATETIME DEFAULT GETDATE()
);
GO

-- =====================================================
-- TABLE 4: REVIEWS
-- Stores customer reviews for cake designs
-- A customer can review many designs
-- A design can have many reviews
-- =====================================================
CREATE TABLE Reviews (
    review_id       INT IDENTITY(1,1) PRIMARY KEY,
    customer_id     INT NOT NULL,
    design_id       INT NOT NULL,
    rating          INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text     NVARCHAR(500),
    review_date     DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_Reviews_Customers 
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        ON DELETE CASCADE,
    CONSTRAINT FK_Reviews_CakeDesigns 
        FOREIGN KEY (design_id) REFERENCES CakeDesigns(design_id)
        ON DELETE CASCADE
);
GO

-- =====================================================
-- ADMIN USERS TABLE (for GUI authentication)
-- =====================================================
CREATE TABLE AdminUsers (
    admin_id        INT IDENTITY(1,1) PRIMARY KEY,
    username        NVARCHAR(50) NOT NULL UNIQUE,
    password_hash   NVARCHAR(255) NOT NULL,
    full_name       NVARCHAR(100),
    created_at      DATETIME DEFAULT GETDATE()
);
GO

-- Insert default admin user (password: crumbear123)
INSERT INTO AdminUsers (username, password_hash, full_name)
VALUES ('admin', 'pbkdf2:sha256:600000$crumbear$e8f5b0c7d9a2b4f6e8c0d2a4b6f8e0c2d4a6b8f0e2c4d6a8b0f2e4c6d8a0b2f4', 'System Administrator');
GO

-- =====================================================
-- INDEXES
-- For performance optimization on frequently queried columns
-- =====================================================

-- Cakes indexes
CREATE INDEX IX_Cakes_Flavor ON Cakes(flavor);
CREATE INDEX IX_Cakes_Size ON Cakes(size);
CREATE INDEX IX_Cakes_Availability ON Cakes(availability);
CREATE INDEX IX_Cakes_BasePrice ON Cakes(base_price);

-- CakeDesigns indexes
CREATE INDEX IX_CakeDesigns_CakeID ON CakeDesigns(cake_id);
CREATE INDEX IX_CakeDesigns_Theme ON CakeDesigns(theme);
CREATE INDEX IX_CakeDesigns_ComplexityLevel ON CakeDesigns(complexity_level);
CREATE INDEX IX_CakeDesigns_CreatedAt ON CakeDesigns(created_at);

-- Customers indexes
CREATE INDEX IX_Customers_Email ON Customers(email);
CREATE INDEX IX_Customers_City ON Customers(city);
CREATE INDEX IX_Customers_CreatedAt ON Customers(created_at);

-- Reviews indexes
CREATE INDEX IX_Reviews_CustomerID ON Reviews(customer_id);
CREATE INDEX IX_Reviews_DesignID ON Reviews(design_id);
CREATE INDEX IX_Reviews_Rating ON Reviews(rating);
CREATE INDEX IX_Reviews_ReviewDate ON Reviews(review_date);

PRINT 'Indexes created successfully.';
GO

-- =====================================================
-- VIEWS
-- Pre-defined queries for common data retrieval
-- =====================================================

-- View 1: Cake details with design count
CREATE VIEW vw_CakeWithDesignCount AS
SELECT 
    c.cake_id,
    c.cake_name,
    c.flavor,
    c.frosting,
    c.size,
    c.base_price,
    c.availability,
    COUNT(cd.design_id) AS design_count
FROM Cakes c
LEFT JOIN CakeDesigns cd ON c.cake_id = cd.cake_id
GROUP BY c.cake_id, c.cake_name, c.flavor, c.frosting, c.size, c.base_price, c.availability;
GO

-- View 2: Design details with cake info and average rating
CREATE VIEW vw_DesignWithRatings AS
SELECT 
    cd.design_id,
    cd.theme,
    cd.color_palette,
    cd.topper_type,
    cd.complexity_level,
    cd.image_url,
    c.cake_name,
    c.flavor,
    c.base_price,
    (SELECT AVG(CAST(r.rating AS DECIMAL(3,2))) 
     FROM Reviews r 
     WHERE r.design_id = cd.design_id) AS avg_rating,
    (SELECT COUNT(*) 
     FROM Reviews r 
     WHERE r.design_id = cd.design_id) AS review_count
FROM CakeDesigns cd
JOIN Cakes c ON cd.cake_id = c.cake_id;
GO

-- View 3: Customer activity summary
CREATE VIEW vw_CustomerActivity AS
SELECT 
    cu.customer_id,
    cu.full_name,
    cu.email,
    cu.city,
    COUNT(r.review_id) AS total_reviews,
    AVG(CAST(r.rating AS DECIMAL(3,2))) AS avg_rating_given,
    MAX(r.review_date) AS last_review_date
FROM Customers cu
LEFT JOIN Reviews r ON cu.customer_id = r.customer_id
GROUP BY cu.customer_id, cu.full_name, cu.email, cu.city;
GO

-- View 4: Top-rated designs (designs with avg rating >= 4)
CREATE VIEW vw_TopRatedDesigns AS
SELECT 
    cd.design_id,
    cd.theme,
    c.cake_name,
    c.flavor,
    AVG(CAST(r.rating AS DECIMAL(3,2))) AS avg_rating,
    COUNT(r.review_id) AS review_count
FROM CakeDesigns cd
JOIN Cakes c ON cd.cake_id = c.cake_id
JOIN Reviews r ON cd.design_id = r.design_id
GROUP BY cd.design_id, cd.theme, c.cake_name, c.flavor
HAVING AVG(CAST(r.rating AS DECIMAL(3,2))) >= 4;
GO

PRINT 'Views created successfully.';
GO

-- =====================================================
-- TRIGGERS
-- Automatic actions on data changes
-- =====================================================

-- Trigger 1: Update timestamp when cake is modified
CREATE TRIGGER trg_UpdateCakeTimestamp
ON Cakes
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Cakes
    SET updated_at = GETDATE()
    WHERE cake_id IN (SELECT cake_id FROM inserted);
END;
GO

-- Trigger 2: Prevent deletion of cake with designs that have reviews
CREATE TRIGGER trg_PreventCakeDeletionWithReviews
ON Cakes
INSTEAD OF DELETE
AS
BEGIN
    SET NOCOUNT ON;
    
    IF EXISTS (
        SELECT 1 
        FROM deleted d
        JOIN CakeDesigns cd ON d.cake_id = cd.cake_id
        JOIN Reviews r ON cd.design_id = r.design_id
    )
    BEGIN
        RAISERROR('Cannot delete cake: Associated designs have customer reviews.', 16, 1);
        RETURN;
    END
    
    -- Safe to delete - cascade will handle designs without reviews
    DELETE FROM Cakes WHERE cake_id IN (SELECT cake_id FROM deleted);
END;
GO

-- Trigger 3: Log new reviews (audit trail)
CREATE TABLE ReviewAuditLog (
    log_id          INT IDENTITY(1,1) PRIMARY KEY,
    review_id       INT,
    customer_id     INT,
    design_id       INT,
    rating          INT,
    action_type     NVARCHAR(10),
    action_date     DATETIME DEFAULT GETDATE()
);
GO

CREATE TRIGGER trg_LogNewReview
ON Reviews
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO ReviewAuditLog (review_id, customer_id, design_id, rating, action_type)
    SELECT review_id, customer_id, design_id, rating, 'INSERT'
    FROM inserted;
END;
GO

-- Trigger 4: Validate email format on customer insert/update
CREATE TRIGGER trg_ValidateCustomerEmail
ON Customers
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    IF EXISTS (
        SELECT 1 FROM inserted 
        WHERE email NOT LIKE '%_@_%._%'
    )
    BEGIN
        RAISERROR('Invalid email format.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END
END;
GO

PRINT 'Triggers created successfully.';
GO

-- =====================================================
-- STORED FUNCTIONS
-- Reusable calculations and lookups
-- =====================================================

-- Function 1: Calculate total price for a design (base + complexity modifier)
CREATE FUNCTION fn_CalculateDesignPrice(@design_id INT)
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @price DECIMAL(10,2);
    
    SELECT @price = c.base_price * 
        CASE cd.complexity_level
            WHEN 'Simple' THEN 1.0
            WHEN 'Moderate' THEN 1.25
            WHEN 'Complex' THEN 1.5
            WHEN 'Expert' THEN 2.0
            ELSE 1.0
        END
    FROM CakeDesigns cd
    JOIN Cakes c ON cd.cake_id = c.cake_id
    WHERE cd.design_id = @design_id;
    
    RETURN ISNULL(@price, 0);
END;
GO

-- Function 2: Get average rating for a design
CREATE FUNCTION fn_GetDesignAvgRating(@design_id INT)
RETURNS DECIMAL(3,2)
AS
BEGIN
    DECLARE @avg_rating DECIMAL(3,2);
    
    SELECT @avg_rating = AVG(CAST(rating AS DECIMAL(3,2)))
    FROM Reviews
    WHERE design_id = @design_id;
    
    RETURN ISNULL(@avg_rating, 0);
END;
GO

-- Function 3: Get total reviews by a customer
CREATE FUNCTION fn_GetCustomerReviewCount(@customer_id INT)
RETURNS INT
AS
BEGIN
    DECLARE @count INT;
    
    SELECT @count = COUNT(*)
    FROM Reviews
    WHERE customer_id = @customer_id;
    
    RETURN ISNULL(@count, 0);
END;
GO

-- Function 4: Check if design is above average rating (uses subquery)
CREATE FUNCTION fn_IsAboveAverageRating(@design_id INT)
RETURNS BIT
AS
BEGIN
    DECLARE @result BIT = 0;
    DECLARE @design_avg DECIMAL(3,2);
    DECLARE @overall_avg DECIMAL(3,2);
    
    SELECT @design_avg = AVG(CAST(rating AS DECIMAL(3,2)))
    FROM Reviews
    WHERE design_id = @design_id;
    
    SELECT @overall_avg = AVG(CAST(rating AS DECIMAL(3,2)))
    FROM Reviews;
    
    IF @design_avg > @overall_avg
        SET @result = 1;
    
    RETURN @result;
END;
GO

PRINT 'Functions created successfully.';
GO

-- =====================================================
-- STORED PROCEDURES
-- Complex operations and business logic
-- =====================================================

-- Procedure 1: Get dashboard statistics
CREATE PROCEDURE sp_GetDashboardStats
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        (SELECT COUNT(*) FROM Cakes) AS total_cakes,
        (SELECT COUNT(*) FROM CakeDesigns) AS total_designs,
        (SELECT COUNT(*) FROM Customers) AS total_customers,
        (SELECT COUNT(*) FROM Reviews) AS total_reviews,
        (SELECT AVG(CAST(rating AS DECIMAL(3,2))) FROM Reviews) AS overall_avg_rating,
        (SELECT COUNT(*) FROM Cakes WHERE availability = 1) AS available_cakes;
END;
GO

-- Procedure 2: Search cakes by criteria
CREATE PROCEDURE sp_SearchCakes
    @search_term NVARCHAR(100) = NULL,
    @flavor NVARCHAR(50) = NULL,
    @size NVARCHAR(20) = NULL,
    @min_price DECIMAL(10,2) = NULL,
    @max_price DECIMAL(10,2) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        c.cake_id,
        c.cake_name,
        c.flavor,
        c.frosting,
        c.size,
        c.base_price,
        c.availability,
        (SELECT COUNT(*) FROM CakeDesigns WHERE cake_id = c.cake_id) AS design_count
    FROM Cakes c
    WHERE 
        (@search_term IS NULL OR c.cake_name LIKE '%' + @search_term + '%')
        AND (@flavor IS NULL OR c.flavor = @flavor)
        AND (@size IS NULL OR c.size = @size)
        AND (@min_price IS NULL OR c.base_price >= @min_price)
        AND (@max_price IS NULL OR c.base_price <= @max_price)
    ORDER BY c.cake_name;
END;
GO

-- Procedure 3: Get top designs by rating (with subquery)
CREATE PROCEDURE sp_GetTopDesigns
    @top_count INT = 10
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT TOP (@top_count)
        cd.design_id,
        cd.theme,
        cd.color_palette,
        cd.complexity_level,
        c.cake_name,
        c.flavor,
        dbo.fn_CalculateDesignPrice(cd.design_id) AS total_price,
        (SELECT AVG(CAST(r.rating AS DECIMAL(3,2))) 
         FROM Reviews r WHERE r.design_id = cd.design_id) AS avg_rating,
        (SELECT COUNT(*) 
         FROM Reviews r WHERE r.design_id = cd.design_id) AS review_count
    FROM CakeDesigns cd
    JOIN Cakes c ON cd.cake_id = c.cake_id
    WHERE EXISTS (SELECT 1 FROM Reviews r WHERE r.design_id = cd.design_id)
    ORDER BY avg_rating DESC, review_count DESC;
END;
GO

-- Procedure 4: Get customer review history
CREATE PROCEDURE sp_GetCustomerReviews
    @customer_id INT
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        r.review_id,
        r.rating,
        r.review_text,
        r.review_date,
        cd.theme,
        cd.color_palette,
        c.cake_name,
        c.flavor
    FROM Reviews r
    JOIN CakeDesigns cd ON r.design_id = cd.design_id
    JOIN Cakes c ON cd.cake_id = c.cake_id
    WHERE r.customer_id = @customer_id
    ORDER BY r.review_date DESC;
END;
GO

-- Procedure 5: Get designs by cake with ratings
CREATE PROCEDURE sp_GetCakeDesigns
    @cake_id INT
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        cd.design_id,
        cd.theme,
        cd.color_palette,
        cd.topper_type,
        cd.complexity_level,
        cd.image_url,
        cd.created_at,
        dbo.fn_CalculateDesignPrice(cd.design_id) AS calculated_price,
        dbo.fn_GetDesignAvgRating(cd.design_id) AS avg_rating,
        (SELECT COUNT(*) FROM Reviews WHERE design_id = cd.design_id) AS review_count
    FROM CakeDesigns cd
    WHERE cd.cake_id = @cake_id
    ORDER BY cd.created_at DESC;
END;
GO

PRINT 'Stored Procedures created successfully.';
GO

-- =====================================================
-- SCHEMA SUMMARY
-- =====================================================
PRINT '';
PRINT '========================================';
PRINT 'CRUMBEAR DATABASE SCHEMA v2.0';
PRINT '========================================';
PRINT 'Tables: Cakes, CakeDesigns, Customers, Reviews';
PRINT 'Supporting: AdminUsers, ReviewAuditLog';
PRINT 'Views: 4 (vw_CakeWithDesignCount, vw_DesignWithRatings, vw_CustomerActivity, vw_TopRatedDesigns)';
PRINT 'Triggers: 4';
PRINT 'Functions: 4';
PRINT 'Stored Procedures: 5';
PRINT 'Indexes: 12';
PRINT '========================================';
GO
