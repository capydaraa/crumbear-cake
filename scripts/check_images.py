#!/usr/bin/env python3
"""Check database for cake images"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))

from db_connection import execute_query

# Check cakes
print("=== CAKES ===")
cakes = execute_query("SELECT cake_id, name FROM Cakes ORDER BY cake_id")
for cake in cakes:
    print(f"  Cake {cake['cake_id']}: {cake['name']}")

# Check cake images
print("\n=== CAKE IMAGES ===")
images = execute_query("SELECT * FROM CakeImages ORDER BY cake_id")
for img in images:
    print(f"  Cake {img['cake_id']}: {img['image_url']} (primary: {img['is_primary']})")

# Check cakes with images
print("\n=== CAKES WITH IMAGE URLS ===")
cakes_with_images = execute_query("""
    SELECT c.cake_id, c.name, 
           (SELECT TOP 1 image_url FROM CakeImages 
            WHERE cake_id = c.cake_id AND is_primary = 1) as image_url
    FROM Cakes c
    ORDER BY c.cake_id
""")
for cake in cakes_with_images:
    print(f"  Cake {cake['cake_id']}: {cake['name']} -> {cake['image_url']}")
