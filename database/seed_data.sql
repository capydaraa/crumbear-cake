-- =====================================================
-- CRUMBEAR CAKE MANAGEMENT SYSTEM - SEED DATA
-- Database: Microsoft SQL Server 2019+
-- Purpose: Generate 1,000-2,000 sample records per table
-- Tables: Cakes (1,000), CakeDesigns (1,500), Customers (1,200), Reviews (2,000)
-- =====================================================

USE CrumbearDB;
GO

-- =====================================================
-- CLEAR EXISTING DATA (in correct order due to FK constraints)
-- =====================================================
PRINT 'Clearing existing data...';

DELETE FROM ReviewAuditLog;
DELETE FROM Reviews;
DELETE FROM CakeDesigns;
DELETE FROM Customers;
DELETE FROM Cakes;
-- Keep AdminUsers as-is

PRINT 'Existing data cleared.';
GO

-- =====================================================
-- 1. CAKES TABLE (1,000 records)
-- =====================================================
PRINT 'Inserting Cakes...';

-- Flavor options
DECLARE @Flavors TABLE (ID INT IDENTITY(1,1), FlavorName NVARCHAR(50));
INSERT INTO @Flavors (FlavorName) VALUES
('Vanilla'), ('Chocolate'), ('Red Velvet'), ('Strawberry'), ('Lemon'),
('Carrot'), ('Coconut'), ('Marble'), ('Funfetti'), ('Banana'),
('Coffee'), ('Almond'), ('Peanut Butter'), ('Cookies & Cream'), ('Mint Chocolate'),
('Orange'), ('Raspberry'), ('Blueberry'), ('Caramel'), ('Cheesecake');

-- Frosting options
DECLARE @Frostings TABLE (ID INT IDENTITY(1,1), FrostingName NVARCHAR(50));
INSERT INTO @Frostings (FrostingName) VALUES
('Buttercream'), ('Cream Cheese'), ('Whipped Cream'), ('Fondant'), ('Ganache'),
('Swiss Meringue'), ('Italian Meringue'), ('Royal Icing'), ('Chocolate Fudge'), ('Caramel Drizzle');

-- Size options
DECLARE @Sizes TABLE (ID INT IDENTITY(1,1), SizeName NVARCHAR(20));
INSERT INTO @Sizes (SizeName) VALUES
('6 inch'), ('8 inch'), ('10 inch'), ('12 inch'), ('Cupcake');

-- Cake name prefixes
DECLARE @Prefixes TABLE (ID INT IDENTITY(1,1), PrefixName NVARCHAR(30));
INSERT INTO @Prefixes (PrefixName) VALUES
('Classic'), ('Deluxe'), ('Premium'), ('Signature'), ('Artisan'),
('Homestyle'), ('Gourmet'), ('Special'), ('Traditional'), ('Modern');

DECLARE @i INT = 1;
DECLARE @FlavorName NVARCHAR(50);
DECLARE @FrostingName NVARCHAR(50);
DECLARE @SizeName NVARCHAR(20);
DECLARE @PrefixName NVARCHAR(30);
DECLARE @BasePrice DECIMAL(10,2);

WHILE @i <= 1000
BEGIN
    SELECT @FlavorName = FlavorName FROM @Flavors WHERE ID = ((@i - 1) % 20) + 1;
    SELECT @FrostingName = FrostingName FROM @Frostings WHERE ID = ((@i - 1) % 10) + 1;
    SELECT @SizeName = SizeName FROM @Sizes WHERE ID = ((@i - 1) % 5) + 1;
    SELECT @PrefixName = PrefixName FROM @Prefixes WHERE ID = ((@i - 1) / 100 % 10) + 1;
    
    -- Price based on size
    SET @BasePrice = CASE @SizeName
        WHEN '6 inch' THEN ROUND(RAND(CHECKSUM(NEWID())) * 15 + 25, 2)    -- $25-40
        WHEN '8 inch' THEN ROUND(RAND(CHECKSUM(NEWID())) * 20 + 35, 2)    -- $35-55
        WHEN '10 inch' THEN ROUND(RAND(CHECKSUM(NEWID())) * 25 + 45, 2)   -- $45-70
        WHEN '12 inch' THEN ROUND(RAND(CHECKSUM(NEWID())) * 30 + 55, 2)   -- $55-85
        ELSE ROUND(RAND(CHECKSUM(NEWID())) * 2 + 3, 2)                     -- $3-5 (cupcake)
    END;
    
    INSERT INTO Cakes (cake_name, flavor, frosting, size, base_price, availability, created_at)
    VALUES (
        @PrefixName + ' ' + @FlavorName + ' Cake',
        @FlavorName,
        @FrostingName,
        @SizeName,
        @BasePrice,
        CASE WHEN RAND(CHECKSUM(NEWID())) > 0.1 THEN 1 ELSE 0 END, -- 90% available
        DATEADD(DAY, -FLOOR(RAND(CHECKSUM(NEWID())) * 365), GETDATE())
    );
    
    SET @i = @i + 1;
END;

PRINT 'Cakes inserted: 1,000 records';
GO

-- =====================================================
-- 2. CAKE_DESIGNS TABLE (1,500 records)
-- =====================================================
PRINT 'Inserting CakeDesigns...';

-- Theme options
DECLARE @Themes TABLE (ID INT IDENTITY(1,1), ThemeName NVARCHAR(100));
INSERT INTO @Themes (ThemeName) VALUES
('Birthday Party'), ('Wedding Elegant'), ('Baby Shower'), ('Anniversary'),
('Graduation'), ('Holiday Special'), ('Valentine Romance'), ('Halloween Spooky'),
('Christmas Joy'), ('Easter Spring'), ('Floral Garden'), ('Rustic Charm'),
('Modern Minimalist'), ('Princess Fantasy'), ('Superhero Adventure'),
('Sports Victory'), ('Unicorn Magic'), ('Ocean Waves'), ('Galaxy Stars'), ('Safari Wild');

-- Color palette options
DECLARE @Colors TABLE (ID INT IDENTITY(1,1), ColorName NVARCHAR(100));
INSERT INTO @Colors (ColorName) VALUES
('Pink & White'), ('Blue & Silver'), ('Gold & Ivory'), ('Red & Black'),
('Pastel Rainbow'), ('Navy & Gold'), ('Lavender & Mint'), ('Rose Gold'),
('Black & White'), ('Green & Brown'), ('Orange & Yellow'), ('Purple & Silver'),
('Teal & Coral'), ('Burgundy & Gold'), ('Peach & Cream');

-- Topper options
DECLARE @Toppers TABLE (ID INT IDENTITY(1,1), TopperName NVARCHAR(50));
INSERT INTO @Toppers (TopperName) VALUES
('Fresh Flowers'), ('Fondant Figures'), ('Cake Topper Sign'), ('Edible Glitter'),
('Chocolate Decorations'), ('Sugar Pearls'), ('Macarons'), ('Berries'),
('Candles'), ('Sparklers'), ('Custom Figurine'), ('Edible Image'), (NULL);

-- Complexity levels
DECLARE @Complexity TABLE (ID INT IDENTITY(1,1), LevelName NVARCHAR(20));
INSERT INTO @Complexity (LevelName) VALUES
('Simple'), ('Simple'), ('Moderate'), ('Moderate'), ('Moderate'), ('Complex'), ('Complex'), ('Expert');

DECLARE @j INT = 1;
DECLARE @CakeID INT;
DECLARE @ThemeName NVARCHAR(100);
DECLARE @ColorName NVARCHAR(100);
DECLARE @TopperName NVARCHAR(50);
DECLARE @ComplexityLevel NVARCHAR(20);
DECLARE @MaxCakes INT;

SELECT @MaxCakes = COUNT(*) FROM Cakes;

WHILE @j <= 1500
BEGIN
    SET @CakeID = ((@j - 1) % @MaxCakes) + 1;
    SELECT @ThemeName = ThemeName FROM @Themes WHERE ID = ((@j - 1) % 20) + 1;
    SELECT @ColorName = ColorName FROM @Colors WHERE ID = ((@j - 1) % 15) + 1;
    SELECT @TopperName = TopperName FROM @Toppers WHERE ID = ((@j - 1) % 13) + 1;
    SELECT @ComplexityLevel = LevelName FROM @Complexity WHERE ID = ((@j - 1) % 8) + 1;
    
    INSERT INTO CakeDesigns (cake_id, theme, color_palette, topper_type, complexity_level, image_url, created_at)
    VALUES (
        @CakeID,
        @ThemeName,
        @ColorName,
        @TopperName,
        @ComplexityLevel,
        '/static/images/cakes/design_' + CAST(@j AS NVARCHAR(10)) + '.jpg',
        DATEADD(DAY, -FLOOR(RAND(CHECKSUM(NEWID())) * 300), GETDATE())
    );
    
    SET @j = @j + 1;
END;

PRINT 'CakeDesigns inserted: 1,500 records';
GO

-- =====================================================
-- 3. CUSTOMERS TABLE (1,200 records)
-- =====================================================
PRINT 'Inserting Customers...';

-- First names
DECLARE @FirstNames TABLE (ID INT IDENTITY(1,1), FirstName NVARCHAR(30));
INSERT INTO @FirstNames (FirstName) VALUES
('Emma'), ('Liam'), ('Olivia'), ('Noah'), ('Ava'), ('Ethan'), ('Sophia'), ('Mason'),
('Isabella'), ('William'), ('Mia'), ('James'), ('Charlotte'), ('Benjamin'), ('Amelia'),
('Lucas'), ('Harper'), ('Henry'), ('Evelyn'), ('Alexander'), ('Luna'), ('Michael'),
('Camila'), ('Daniel'), ('Gianna'), ('Matthew'), ('Aria'), ('David'), ('Ella'), ('Joseph');

-- Last names
DECLARE @LastNames TABLE (ID INT IDENTITY(1,1), LastName NVARCHAR(30));
INSERT INTO @LastNames (LastName) VALUES
('Smith'), ('Johnson'), ('Williams'), ('Brown'), ('Jones'), ('Garcia'), ('Miller'),
('Davis'), ('Rodriguez'), ('Martinez'), ('Hernandez'), ('Lopez'), ('Gonzalez'),
('Wilson'), ('Anderson'), ('Thomas'), ('Taylor'), ('Moore'), ('Jackson'), ('Martin'),
('Lee'), ('Perez'), ('Thompson'), ('White'), ('Harris'), ('Sanchez'), ('Clark'),
('Ramirez'), ('Lewis'), ('Robinson'), ('Walker'), ('Young'), ('Allen'), ('King'), ('Wright');

-- Cities
DECLARE @Cities TABLE (ID INT IDENTITY(1,1), CityName NVARCHAR(50));
INSERT INTO @Cities (CityName) VALUES
('New York'), ('Los Angeles'), ('Chicago'), ('Houston'), ('Phoenix'),
('Philadelphia'), ('San Antonio'), ('San Diego'), ('Dallas'), ('San Jose'),
('Austin'), ('Jacksonville'), ('Fort Worth'), ('Columbus'), ('Charlotte'),
('Seattle'), ('Denver'), ('Boston'), ('Portland'), ('Miami');

DECLARE @k INT = 1;
DECLARE @FirstName NVARCHAR(30);
DECLARE @LastName NVARCHAR(30);
DECLARE @CityName NVARCHAR(50);
DECLARE @Email NVARCHAR(100);

WHILE @k <= 1200
BEGIN
    SELECT @FirstName = FirstName FROM @FirstNames WHERE ID = ((@k - 1) % 30) + 1;
    SELECT @LastName = LastName FROM @LastNames WHERE ID = ((@k - 1) % 35) + 1;
    SELECT @CityName = CityName FROM @Cities WHERE ID = ((@k - 1) % 20) + 1;
    
    SET @Email = LOWER(@FirstName) + '.' + LOWER(@LastName) + CAST(@k AS NVARCHAR(10)) + '@email.com';
    
    INSERT INTO Customers (full_name, email, city, created_at)
    VALUES (
        @FirstName + ' ' + @LastName,
        @Email,
        @CityName,
        DATEADD(DAY, -FLOOR(RAND(CHECKSUM(NEWID())) * 400), GETDATE())
    );
    
    SET @k = @k + 1;
END;

PRINT 'Customers inserted: 1,200 records';
GO

-- =====================================================
-- 4. REVIEWS TABLE (2,000 records)
-- =====================================================
PRINT 'Inserting Reviews...';

-- Review text templates
DECLARE @ReviewTexts TABLE (ID INT IDENTITY(1,1), ReviewText NVARCHAR(500));
INSERT INTO @ReviewTexts (ReviewText) VALUES
('Absolutely delicious! The cake was moist and the frosting was perfect.'),
('Beautiful design and tasted amazing. Will order again!'),
('Good cake but delivery was a bit late.'),
('Perfect for my daughter''s birthday. Everyone loved it!'),
('The flavors were incredible. Highly recommend!'),
('Exceeded my expectations. The attention to detail was impressive.'),
('Great quality for the price. Very satisfied.'),
('The cake was fresh and the design matched exactly what I wanted.'),
('A bit too sweet for my taste, but the design was gorgeous.'),
('Best cake I''ve ever had! The texture was perfect.'),
('Wonderful service and the cake was a hit at the party!'),
('The decorations were stunning. Worth every penny.'),
('Good cake, but I expected a bit more flavor.'),
('Amazing! The fondant work was professional quality.'),
('Ordered for my wedding and it was absolutely perfect!'),
('Tasty and beautiful. My guests couldn''t stop complimenting it.'),
('The cream cheese frosting was to die for!'),
('Lovely presentation and even better taste.'),
('Would definitely recommend to friends and family.'),
('The cake arrived in perfect condition and tasted fresh.');

DECLARE @m INT = 1;
DECLARE @CustomerID INT;
DECLARE @DesignID INT;
DECLARE @Rating INT;
DECLARE @ReviewText NVARCHAR(500);
DECLARE @MaxCustomers INT;
DECLARE @MaxDesigns INT;

SELECT @MaxCustomers = COUNT(*) FROM Customers;
SELECT @MaxDesigns = COUNT(*) FROM CakeDesigns;

WHILE @m <= 2000
BEGIN
    SET @CustomerID = FLOOR(RAND(CHECKSUM(NEWID())) * @MaxCustomers) + 1;
    SET @DesignID = FLOOR(RAND(CHECKSUM(NEWID())) * @MaxDesigns) + 1;
    
    -- Weighted rating (more 4s and 5s to simulate realistic reviews)
    SET @Rating = CASE 
        WHEN RAND(CHECKSUM(NEWID())) < 0.05 THEN 1  -- 5%
        WHEN RAND(CHECKSUM(NEWID())) < 0.15 THEN 2  -- 10%
        WHEN RAND(CHECKSUM(NEWID())) < 0.35 THEN 3  -- 20%
        WHEN RAND(CHECKSUM(NEWID())) < 0.65 THEN 4  -- 30%
        ELSE 5                                       -- 35%
    END;
    
    SELECT @ReviewText = ReviewText FROM @ReviewTexts WHERE ID = ((@m - 1) % 20) + 1;
    
    INSERT INTO Reviews (customer_id, design_id, rating, review_text, review_date)
    VALUES (
        @CustomerID,
        @DesignID,
        @Rating,
        @ReviewText,
        DATEADD(DAY, -FLOOR(RAND(CHECKSUM(NEWID())) * 200), GETDATE())
    );
    
    SET @m = @m + 1;
END;

PRINT 'Reviews inserted: 2,000 records';
GO

-- =====================================================
-- VERIFY DATA COUNTS
-- =====================================================
PRINT '';
PRINT '========================================';
PRINT 'SEED DATA SUMMARY';
PRINT '========================================';

SELECT 'Cakes' AS TableName, COUNT(*) AS RecordCount FROM Cakes
UNION ALL
SELECT 'CakeDesigns', COUNT(*) FROM CakeDesigns
UNION ALL
SELECT 'Customers', COUNT(*) FROM Customers
UNION ALL
SELECT 'Reviews', COUNT(*) FROM Reviews
UNION ALL
SELECT 'ReviewAuditLog', COUNT(*) FROM ReviewAuditLog
UNION ALL
SELECT 'AdminUsers', COUNT(*) FROM AdminUsers;

PRINT '';
PRINT 'Seed data generation complete!';
PRINT '========================================';
GO
