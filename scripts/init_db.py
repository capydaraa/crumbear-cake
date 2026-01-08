#!/usr/bin/env python3
"""
Initialize Crumbear Database
============================
This script creates the database schema and optionally seeds initial data.
Run with: python scripts/init_db.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))

import pyodbc
from db_connection import execute_query, execute_insert, get_db_connection, DB_CONFIG

def create_database():
    """Create the database if it doesn't exist"""
    print("🔧 Checking database existence...")
    
    # Connect to master database
    master_conn_str = (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE=master;"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']};"
        f"TrustServerCertificate=yes;"
        f"Encrypt=yes;"
    )
    
    try:
        conn = pyodbc.connect(master_conn_str, autocommit=True)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT DB_ID('{DB_CONFIG['database']}')")
        result = cursor.fetchone()
        
        if result[0] is None:
            print(f"  - Creating database {DB_CONFIG['database']}...")
            cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
            print(f"  ✅ Database created!")
        else:
            print(f"  ✅ Database {DB_CONFIG['database']} already exists")
        
        conn.close()
        return True
    except pyodbc.Error as e:
        print(f"  ❌ Error creating database: {e}")
        return False

def execute_sql_file(filepath):
    """Execute a SQL file"""
    print(f"  - Executing {os.path.basename(filepath)}...")
    
    with open(filepath, 'r') as f:
        sql_content = f.read()
    
    # Split by GO statements (SQL Server batch separator)
    batches = sql_content.split('\nGO\n')
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        for batch in batches:
            batch = batch.strip()
            if batch and not batch.startswith('--'):
                try:
                    cursor.execute(batch)
                    conn.commit()
                except pyodbc.Error as e:
                    # Some errors are expected (e.g., IF EXISTS checks)
                    if 'already exists' not in str(e).lower():
                        print(f"    Warning: {str(e)[:100]}")

def init_database():
    """Initialize the database with schema"""
    print("\n" + "=" * 60)
    print("CRUMBEAR DATABASE INITIALIZATION")
    print("=" * 60)
    
    # Step 1: Create database
    if not create_database():
        print("❌ Failed to create database")
        return False
    
    # Step 2: Execute schema
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
    if os.path.exists(schema_path):
        print("\n📋 Creating schema...")
        execute_sql_file(schema_path)
        print("  ✅ Schema created!")
    else:
        print(f"  ⚠️ Schema file not found: {schema_path}")
    
    # Step 3: Insert minimum seed data for testing (NOT the full 1000+ records)
    print("\n🌱 Inserting minimum seed data...")
    insert_minimum_seed_data()
    
    print("\n" + "=" * 60)
    print("✅ Database initialization complete!")
    print("=" * 60)
    return True

def insert_minimum_seed_data():
    """Insert minimum data needed for testing (admin user, few records)"""
    try:
        # Check if AdminUsers exists and has data
        existing = execute_query("SELECT COUNT(*) as cnt FROM AdminUsers")
        if existing and existing[0]['cnt'] > 0:
            print("  ✅ Admin users already exist")
        else:
            # Insert admin user
            execute_insert("""
                INSERT INTO AdminUsers (username, password_hash, email, full_name)
                VALUES ('admin', 'crumbear123_hash', 'admin@crumbear.com', 'System Admin')
            """)
            print("  ✅ Admin user created (username: admin)")
        
        # Check if we have some cakes
        cakes = execute_query("SELECT COUNT(*) as cnt FROM Cakes")
        if cakes and cakes[0]['cnt'] == 0:
            # Insert a few sample cakes
            sample_cakes = [
                ('Classic Vanilla', 'Vanilla', 'Buttercream', 'Medium', 1200.00, 1),
                ('Chocolate Dream', 'Chocolate', 'Ganache', 'Large', 1500.00, 1),
                ('Red Velvet', 'Red Velvet', 'Cream Cheese', 'Medium', 1400.00, 1),
                ('Ube Delight', 'Ube', 'Buttercream', 'Small', 1000.00, 1),
                ('Mango Cream', 'Mango', 'Whipped Cream', 'Medium', 1300.00, 1),
            ]
            for cake in sample_cakes:
                execute_insert("""
                    INSERT INTO Cakes (cake_name, flavor, frosting, size, base_price, availability)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, cake)
            print(f"  ✅ {len(sample_cakes)} sample cakes created")
        else:
            print(f"  ✅ Cakes already exist ({cakes[0]['cnt']} records)")
        
        # Check if we have some designs
        designs = execute_query("SELECT COUNT(*) as cnt FROM CakeDesigns")
        if designs and designs[0]['cnt'] == 0:
            # Insert sample designs linked to cakes
            sample_designs = [
                (1, 'Birthday Celebration', 'Pink, Gold, White', 'Candles', 'Simple'),
                (1, 'Elegant White', 'White, Silver', 'Flowers', 'Moderate'),
                (2, 'Chocolate Ganache Drip', 'Brown, Gold', 'Berries', 'Complex'),
                (3, 'Classic Red Velvet', 'Red, White, Gold', 'Heart Topper', 'Moderate'),
                (4, 'Purple Dream', 'Purple, Lavender, White', 'Flowers', 'Simple'),
            ]
            for design in sample_designs:
                execute_insert("""
                    INSERT INTO CakeDesigns (cake_id, theme, color_palette, topper_type, complexity_level, image_url)
                    VALUES (?, ?, ?, ?, ?, 'https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=800')
                """, design)
            print(f"  ✅ {len(sample_designs)} sample designs created")
        else:
            print(f"  ✅ Designs already exist ({designs[0]['cnt']} records)")
        
        # Check if we have some customers
        customers = execute_query("SELECT COUNT(*) as cnt FROM Customers")
        if customers and customers[0]['cnt'] == 0:
            sample_customers = [
                ('Maria Santos', 'maria@example.com', 'Manila'),
                ('Juan Cruz', 'juan@example.com', 'Quezon City'),
                ('Ana Reyes', 'ana@example.com', 'Makati'),
            ]
            for customer in sample_customers:
                execute_insert("""
                    INSERT INTO Customers (full_name, email, city)
                    VALUES (?, ?, ?)
                """, customer)
            print(f"  ✅ {len(sample_customers)} sample customers created")
        else:
            print(f"  ✅ Customers already exist ({customers[0]['cnt']} records)")
        
        # Check if we have some reviews
        reviews = execute_query("SELECT COUNT(*) as cnt FROM Reviews")
        if reviews and reviews[0]['cnt'] == 0:
            sample_reviews = [
                (1, 1, 5, 'Absolutely loved this cake! Perfect for my birthday.'),
                (2, 2, 4, 'Very elegant design, great taste.'),
                (3, 3, 5, 'The chocolate was amazing!'),
            ]
            for review in sample_reviews:
                execute_insert("""
                    INSERT INTO Reviews (customer_id, design_id, rating, review_text)
                    VALUES (?, ?, ?, ?)
                """, review)
            print(f"  ✅ {len(sample_reviews)} sample reviews created")
        else:
            print(f"  ✅ Reviews already exist ({reviews[0]['cnt']} records)")
            
    except Exception as e:
        print(f"  ⚠️ Error inserting seed data: {e}")

def verify_database():
    """Verify database structure"""
    print("\n📊 Verifying database structure...")
    
    try:
        # Check tables
        tables = execute_query("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        print(f"  Tables: {[t['TABLE_NAME'] for t in tables]}")
        
        # Check record counts
        for table in ['Cakes', 'CakeDesigns', 'Customers', 'Reviews']:
            count = execute_query(f"SELECT COUNT(*) as cnt FROM {table}")
            print(f"    - {table}: {count[0]['cnt']} records")
        
        # Check views
        views = execute_query("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.VIEWS
            ORDER BY TABLE_NAME
        """)
        print(f"  Views: {[v['TABLE_NAME'] for v in views]}")
        
        # Check stored procedures
        procs = execute_query("""
            SELECT ROUTINE_NAME 
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_TYPE = 'PROCEDURE'
            ORDER BY ROUTINE_NAME
        """)
        print(f"  Stored Procedures: {[p['ROUTINE_NAME'] for p in procs]}")
        
        # Check functions
        funcs = execute_query("""
            SELECT ROUTINE_NAME 
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_TYPE = 'FUNCTION'
            ORDER BY ROUTINE_NAME
        """)
        print(f"  Functions: {[f['ROUTINE_NAME'] for f in funcs]}")
        
        print("  ✅ Verification complete!")
        
    except Exception as e:
        print(f"  ❌ Verification error: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Initialize Crumbear Database')
    parser.add_argument('--verify', action='store_true', help='Only verify existing database')
    args = parser.parse_args()
    
    if args.verify:
        verify_database()
    else:
        init_database()
        verify_database()
