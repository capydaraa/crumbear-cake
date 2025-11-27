# Crumbear UI Setup Instructions

## 📸 Add Your Logo

Please add your Crumbear logo image to:
```
/Users/bubby/Desktop/ADS/frontend/static/images/logo.png
```

The logo from your screenshot should be saved there.

## 🖼️ Add Cake Images (Optional)

For placeholder cake images, you can:
1. Add images to: `/Users/bubby/Desktop/ADS/frontend/static/images/`
2. Or use the placeholder that will be created automatically

## 🚀 Preview the UI

### Step 1: Install Flask
```bash
cd /Users/bubby/Desktop/ADS
pip3 install -r requirements.txt
```

### Step 2: Run the preview app
```bash
python3 preview_app.py
```

### Step 3: Open in browser
Navigate to: `http://localhost:5000`

## 📄 Pages Available:

1. **Home/Browse Cakes**: `http://localhost:5000/`
2. **Price Calculator**: `http://localhost:5000/calculator`
3. **Admin Login**: `http://localhost:5000/admin/login`

## 🎨 Design Features:

✅ Pink Crumbear theme matching your Framer design
✅ Scalloped decorative border
✅ Category filtering (Birthday, Wedding, Anniversaries, Cartoons)
✅ Interactive price calculator with:
   - Size selection (4x3, 5x3, 6x3)
   - Layer selection (1-5)
   - Flavor selection
   - 10+ toppings with quantities
   - Icing colors for 3 parts (Base, Sides, Other)
   - Each color has 3 shades (Light, Medium, Dark)
   - Message on cake option (+₱50)
   - Rush order option (×1.5)
   - Real-time price calculation
✅ Responsive design
✅ Smooth animations
✅ Bootstrap 5 framework

## 📝 Next Steps:

After previewing the UI, we'll:
1. Create the database schema
2. Build the backend API with Flask
3. Connect frontend to real database
4. Add admin dashboard with charts
5. Generate sample data (1000-2000 records)
6. Implement advanced SQL features

## 💡 Tips:

- The preview app uses mock data
- Calculator fully functional with real-time price updates
- All forms have validation
- Mobile responsive
