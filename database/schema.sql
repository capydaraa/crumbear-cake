-- Crumbear Cake Management System - Database Schema
-- Microsoft SQL Server 2019+
-- Created: November 27, 2025

USE CrumbearDB;
GO

-- Drop existing tables (in reverse order of dependencies)
IF OBJECT_ID('EstimateIcing', 'U') IS NOT NULL DROP TABLE EstimateIcing;
IF OBJECT_ID('EstimateToppings', 'U') IS NOT NULL DROP TABLE EstimateToppings;
IF OBJECT_ID('PriceEstimates', 'U') IS NOT NULL DROP TABLE PriceEstimates;
IF OBJECT_ID('CakeImages', 'U') IS NOT NULL DROP TABLE CakeImages;
IF OBJECT_ID('Cakes', 'U') IS NOT NULL DROP TABLE Cakes;
IF OBJECT_ID('Flavors', 'U') IS NOT NULL DROP TABLE Flavors;
IF OBJECT_ID('Toppings', 'U') IS NOT NULL DROP TABLE Toppings;
IF OBJECT_ID('IcingColors', 'U') IS NOT NULL DROP TABLE IcingColors;
IF OBJECT_ID('AdminUsers', 'U') IS NOT NULL DROP TABLE AdminUsers;
GO

-- ====================
-- 1. Cakes Table
-- ====================
CREATE TABLE Cakes (
    cake_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    description NVARCHAR(MAX),
    category NVARCHAR(50) NOT NULL CHECK (category IN ('Birthday', 'Wedding', 'Anniversaries', 'Cartoons', 'Other')),
    base_price_4x3 DECIMAL(10,2) NOT NULL CHECK (base_price_4x3 >= 0),
    base_price_5x3 DECIMAL(10,2) NOT NULL CHECK (base_price_5x3 >= 0),
    base_price_6x3 DECIMAL(10,2) NOT NULL CHECK (base_price_6x3 >= 0),
    is_featured BIT DEFAULT 0,
    view_count INT DEFAULT 0 CHECK (view_count >= 0),
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);
GO

-- ====================
-- 2. CakeImages Table (Support multiple images per cake)
-- ====================
CREATE TABLE CakeImages (
    image_id INT IDENTITY(1,1) PRIMARY KEY,
    cake_id INT NOT NULL,
    image_url NVARCHAR(500) NOT NULL,
    is_primary BIT DEFAULT 0,
    display_order INT DEFAULT 0,
    uploaded_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (cake_id) REFERENCES Cakes(cake_id) ON DELETE CASCADE
);
GO

-- ====================
-- 3. Toppings Table
-- ====================
CREATE TABLE Toppings (
    topping_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    is_available BIT DEFAULT 1,
    image_url NVARCHAR(500),
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- ====================
-- 4. IcingColors Table
-- ====================
CREATE TABLE IcingColors (
    color_id INT IDENTITY(1,1) PRIMARY KEY,
    color_name NVARCHAR(50) NOT NULL,
    hex_code NVARCHAR(7),
    shade NVARCHAR(20) CHECK (shade IN ('Light', 'Medium', 'Dark')),
    price_multiplier DECIMAL(5,2) DEFAULT 1.0 CHECK (price_multiplier > 0),
    is_available BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- ====================
-- 5. Flavors Table
-- ====================
CREATE TABLE Flavors (
    flavor_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL UNIQUE,
    price_per_layer DECIMAL(10,2) NOT NULL CHECK (price_per_layer >= 0),
    is_available BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- ====================
-- 6. PriceEstimates Table
-- ====================
CREATE TABLE PriceEstimates (
    estimate_id INT IDENTITY(1,1) PRIMARY KEY,
    cake_id INT NULL, -- NULL if custom cake
    size NVARCHAR(10) NOT NULL CHECK (size IN ('4x3', '5x3', '6x3')),
    num_layers INT NOT NULL CHECK (num_layers > 0),
    flavor_id INT NOT NULL,
    has_message BIT DEFAULT 0,
    is_rush BIT DEFAULT 0,
    total_price DECIMAL(10,2) NOT NULL CHECK (total_price >= 0),
    estimate_date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (cake_id) REFERENCES Cakes(cake_id) ON DELETE SET NULL,
    FOREIGN KEY (flavor_id) REFERENCES Flavors(flavor_id)
);
GO

-- ====================
-- 7. EstimateToppings Table (Junction)
-- ====================
CREATE TABLE EstimateToppings (
    estimate_topping_id INT IDENTITY(1,1) PRIMARY KEY,
    estimate_id INT NOT NULL,
    topping_id INT NOT NULL,
    quantity INT DEFAULT 1 CHECK (quantity > 0),
    FOREIGN KEY (estimate_id) REFERENCES PriceEstimates(estimate_id) ON DELETE CASCADE,
    FOREIGN KEY (topping_id) REFERENCES Toppings(topping_id)
);
GO

-- ====================
-- 8. EstimateIcing Table (Junction for icing parts)
-- ====================
CREATE TABLE EstimateIcing (
    estimate_icing_id INT IDENTITY(1,1) PRIMARY KEY,
    estimate_id INT NOT NULL,
    icing_part NVARCHAR(20) NOT NULL CHECK (icing_part IN ('Base', 'Sides', 'Other')),
    color_id INT NOT NULL,
    FOREIGN KEY (estimate_id) REFERENCES PriceEstimates(estimate_id) ON DELETE CASCADE,
    FOREIGN KEY (color_id) REFERENCES IcingColors(color_id)
);
GO

-- ====================
-- 9. AdminUsers Table
-- ====================
CREATE TABLE AdminUsers (
    admin_id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- Create indexes for better performance
CREATE INDEX idx_cakes_category ON Cakes(category);
CREATE INDEX idx_cakes_view_count ON Cakes(view_count DESC);
CREATE INDEX idx_cakeimages_cakeid ON CakeImages(cake_id);
CREATE INDEX idx_estimates_date ON PriceEstimates(estimate_date DESC);
GO

PRINT 'Database schema created successfully!';
