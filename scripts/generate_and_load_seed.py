#!/usr/bin/env python3
"""
Generate and load seed data directly into the database
"""

import random
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))

import pyodbc
from db_connection import DB_CONFIG

def get_connection():
    conn_str = (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE=CrumbearDB;"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']};"
        f"TrustServerCertificate=yes;"
        f"Encrypt=yes;"
    )
    return pyodbc.connect(conn_str, autocommit=True)

def load_cake_designs(conn):
    """Generate and load 1000 cake designs"""
    cursor = conn.cursor()
    
    print("Loading CakeDesigns...")
    cursor.execute("DELETE FROM CakeDesigns")
    cursor.execute("DBCC CHECKIDENT ('CakeDesigns', RESEED, 0)")
    
    themes = [
        'Cinnamoroll Dream', 'We Bare Bears', 'Hello Kitty', 'Totoro Magic', 'My Melody', 
        'Kuromi Gothic', 'Pompompurin', 'Gudetama Lazy', 'Pusheen Cat', 'Rilakkuma',
        'Minimalist White', 'Rustic Floral', 'Elegant Rose', 'Garden Party', 'Boho Chic',
        'Birthday Bash', 'Princess Dream', 'Superhero', 'Frozen Magic', 'Unicorn Rainbow',
        'Galaxy Space', 'Mermaid Sea', 'Safari Adventure', 'Dinosaur Land', 'Sports Star',
        'Music Notes', 'Art Palette', 'Travel World', 'Graduation', 'Anniversary Love',
        'Korean Minimal', 'Japanese Zen', 'Vintage Classic', 'Modern Abstract', 'Geometric',
        'Watercolor Art', 'Gold Luxury', 'Silver Elegance', 'Rose Gold Glam', 'Tropical'
    ]
    
    colors = [
        'Pink, White, Gold', 'Blue, White, Silver', 'Red, White, Black', 'Purple, Lavender',
        'Green, White, Brown', 'Yellow, Orange, White', 'Brown, Cream, Gold', 'Gray, White, Pink',
        'Pastel Rainbow', 'Navy, Gold, White', 'Rose Gold, Blush', 'Mint, Coral, White'
    ]
    
    toppers = [
        'Fondant Figure', 'Fresh Flowers', 'Candles', 'Cake Topper', 'Edible Image',
        'Macarons', 'Chocolate Drip', 'Berries', 'Gold Leaf', 'Sprinkles', None
    ]
    
    complexities = ['Simple', 'Moderate', 'Complex', 'Expert']
    
    for i in range(1000):
        cake_id = random.randint(1, 720)
        theme = f"{random.choice(themes)} {random.randint(1, 100)}"
        color = random.choice(colors)
        topper = random.choice(toppers)
        complexity = random.choice(complexities)
        image_url = f"https://images.unsplash.com/photo-{random.randint(1000000, 9999999)}?w=400"
        
        cursor.execute("""
            INSERT INTO CakeDesigns (cake_id, theme, color_palette, topper_type, complexity_level, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (cake_id, theme, color, topper, complexity, image_url))
    
    cursor.execute("SELECT COUNT(*) FROM CakeDesigns")
    print(f"  ✅ CakeDesigns: {cursor.fetchone()[0]} records")

def load_customers(conn):
    """Generate and load 1100 customers"""
    cursor = conn.cursor()
    
    print("Loading Customers...")
    cursor.execute("DELETE FROM Customers")
    cursor.execute("DBCC CHECKIDENT ('Customers', RESEED, 0)")
    
    # Pet-like names (40%)
    pet_names = [
        'Bubbles', 'Mochi', 'Cookie', 'Pudding', 'Peaches', 'Honey', 'Caramel', 'Brownie',
        'Marshmallow', 'Sprinkles', 'Cupcake', 'Biscuit', 'Maple', 'Cinnamon', 'Ginger',
        'Butterscotch', 'Toffee', 'Peanut', 'Nugget', 'Waffles', 'Pancake', 'Muffin',
        'Churro', 'Donut', 'Pretzel', 'Twix', 'Snickers', 'Oreo', 'Skittles', 'Jellybean',
        'Pixie', 'Daisy', 'Lily', 'Rose', 'Willow', 'Poppy', 'Luna', 'Star', 'Cloud', 'Sky',
        'Ruby', 'Pearl', 'Jade', 'Opal', 'Amber', 'Coral', 'Clover', 'Fern', 'Sage', 'Basil'
    ]
    
    # Filipino first names (60%)
    filipino_first = [
        'Maria', 'Juan', 'Jose', 'Ana', 'Pedro', 'Rosa', 'Antonio', 'Carmen', 'Francisco', 'Elena',
        'Carlos', 'Luz', 'Manuel', 'Teresa', 'Luis', 'Corazon', 'Miguel', 'Esperanza', 'Rafael', 'Gloria',
        'Gabriel', 'Fe', 'Ramon', 'Mercy', 'Eduardo', 'Grace', 'Roberto', 'Joy', 'Fernando', 'Hope',
        'Paolo', 'Kristine', 'Mark', 'Nicole', 'John', 'Angela', 'Michael', 'Michelle', 'James', 'Patricia',
        'Mary Grace', 'John Paul', 'Maria Clara', 'Jose Rizal', 'Juan Carlo', 'Ana Maria', 'Maria Luisa'
    ]
    
    filipino_last = [
        'Santos', 'Reyes', 'Cruz', 'Garcia', 'Torres', 'Ramos', 'Rivera', 'Lopez', 'Gonzales', 'Hernandez',
        'Dela Cruz', 'Bautista', 'Aquino', 'Fernandez', 'Mendoza', 'Villanueva', 'Castillo', 'Martinez',
        'Dizon', 'Soriano', 'Tan', 'Lim', 'Chua', 'Ong', 'Go', 'Sy', 'Lee', 'Yap', 'Co', 'Dy',
        'Marquez', 'Navarro', 'Pascual', 'Aguilar', 'Flores', 'Salazar', 'Espinosa', 'Vargas', 'Morales'
    ]
    
    cities = ['Zamboanga City'] * 85 + [
        'Manila', 'Cebu City', 'Davao City', 'Quezon City', 'Makati', 
        'Taguig', 'Pasig', 'Iloilo City', 'Cagayan de Oro', 'Bacolod'
    ] * 15
    
    domains = ['gmail.com', 'yahoo.com', 'outlook.com']
    used_emails = set()
    
    for i in range(1100):
        # 40% pet names, 60% Filipino names
        if random.random() < 0.4:
            name = f"{random.choice(pet_names)} {random.choice(filipino_last)}"
        else:
            name = f"{random.choice(filipino_first)} {random.choice(filipino_last)}"
        
        # Generate unique email
        base_email = name.lower().replace(' ', '.').replace("'", "")
        email = f"{base_email}@{random.choice(domains)}"
        counter = 1
        while email in used_emails:
            email = f"{base_email}{counter}@{random.choice(domains)}"
            counter += 1
        used_emails.add(email)
        
        city = random.choice(cities)
        
        cursor.execute("""
            INSERT INTO Customers (full_name, email, city)
            VALUES (?, ?, ?)
        """, (name, email, city))
    
    cursor.execute("SELECT COUNT(*) FROM Customers")
    print(f"  ✅ Customers: {cursor.fetchone()[0]} records")

def load_reviews(conn):
    """Generate and load 1100 reviews"""
    cursor = conn.cursor()
    
    print("Loading Reviews...")
    cursor.execute("DELETE FROM Reviews")
    cursor.execute("DBCC CHECKIDENT ('Reviews', RESEED, 0)")
    
    # Good reviews (80%)
    good_reviews = [
        "Absolutely stunning cake! Perfect for our celebration.",
        "The design exceeded all expectations! Will order again.",
        "Sobrang ganda! Ang sarap din! Worth every peso.",
        "Best cake shop in Zamboanga! Highly recommended!",
        "Grabe ka nindot! Everyone at the party loved it!",
        "Bien bonito el cake! Gracias Crumbear!",
        "Super satisfied with my order! Amazing quality!",
        "The attention to detail is incredible!",
        "Nalipay kaayo ang celebrant! Perfect design!",
        "OMG so beautiful! Exactly what I wanted!",
        "Ang ganda ng design! Super talented ng baker!",
        "My daughter loved her birthday cake! Thank you!",
        "Professional quality at reasonable price!",
        "The flavor was amazing! Will definitely come back!",
        "Muy sabroso y bonito! El mejor!",
    ]
    
    # Bad reviews (10%)
    bad_reviews = [
        "Cake arrived late and the design was different from what I ordered.",
        "Hindi masarap. Expected better for the price.",
        "Delivery was 3 hours late. Disappointed.",
        "Design was not what I requested. Wrong color.",
        "Sobrang tamis! Not balanced at all.",
        "Fondant was too thick. Couldn't taste the cake.",
        "Wa nindot! Layo sa expectations ko!",
        "Overpriced for basic quality.",
    ]
    
    # Witty reviews (10%)
    witty_reviews = [
        "This cake is so good, I'm considering leaving my boyfriend for it!",
        "My diet said no but my heart said Crumbear. Heart wins!",
        "Sabi ko diet na this year. 2027 na lang diet ko!",
        "This cake fixed my trust issues. Finally something that delivers!",
        "Kinain ko mag-isa sa car. No witnesses. No regrets.",
        "My therapist asked what makes me happy. Showed her this cake.",
        "Wa ko boyfriend pero naay Crumbear! Mas sweet pa jud!",
        "My love language is receiving Crumbear cakes!",
    ]
    
    # Use customers 1-1000 (leave ~100 without reviews)
    customer_ids = list(range(1, 1001))
    random.shuffle(customer_ids)
    
    for i in range(1100):
        customer_id = customer_ids[i % len(customer_ids)]
        design_id = random.randint(1, 1000)
        
        # 80% good, 10% bad, 10% witty
        rand = random.random()
        if rand < 0.8:
            review_text = random.choice(good_reviews)
            rating = random.choice([4, 5, 5, 5])  # Mostly 5s
        elif rand < 0.9:
            review_text = random.choice(bad_reviews)
            rating = random.choice([1, 2, 2])
        else:
            review_text = random.choice(witty_reviews)
            rating = random.choice([4, 5, 5])
        
        cursor.execute("""
            INSERT INTO Reviews (customer_id, design_id, rating, review_text)
            VALUES (?, ?, ?, ?)
        """, (customer_id, design_id, rating, review_text))
    
    cursor.execute("SELECT COUNT(*) FROM Reviews")
    print(f"  ✅ Reviews: {cursor.fetchone()[0]} records")

def main():
    print("\n" + "=" * 50)
    print("LOADING SEED DATA")
    print("=" * 50 + "\n")
    
    conn = get_connection()
    
    # Check existing Cakes
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Cakes")
    cakes_count = cursor.fetchone()[0]
    print(f"Existing Cakes: {cakes_count}")
    
    if cakes_count == 0:
        print("⚠️ No cakes found! Please load seed_cakes.sql first.")
        return
    
    load_cake_designs(conn)
    load_customers(conn)
    load_reviews(conn)
    
    print("\n" + "=" * 50)
    print("✅ SEED DATA LOADED SUCCESSFULLY!")
    print("=" * 50)
    
    # Final counts
    cursor.execute("SELECT COUNT(*) FROM Cakes")
    print(f"\n📊 Final counts:")
    print(f"   Cakes: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM CakeDesigns")
    print(f"   CakeDesigns: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM Customers")
    print(f"   Customers: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM Reviews")
    print(f"   Reviews: {cursor.fetchone()[0]}")
    
    conn.close()

if __name__ == "__main__":
    main()
