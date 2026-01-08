// Price Calculator Logic for Crumbear Cakes

let calculatorState = {
    size: null,
    basePrice: 0,
    numLayers: 1,
    flavorId: null,
    flavorPricePerLayer: 0,
    toppings: [] // {id, name, price, quantity}
};

// Initialize calculator
document.addEventListener('DOMContentLoaded', function() {
    console.log('Calculator initialized');
    
    // Load data from API
    loadSizes();
    loadFlavors();
    loadToppings();
    
    // Set up event listeners
    setupLayerSelection();
    setupFlavorSelection();
});

// ========================================
// Load Data from API
// ========================================

async function loadSizes() {
    try {
        const response = await fetch('/api/sizes');
        const sizes = await response.json();
        renderSizes(sizes);
    } catch (error) {
        console.log('Using mock data for sizes');
        // Mock data fallback
        const mockSizes = [
            {size_id: 1, name: '4x3', description: '4 inches diameter, 3 inches height', base_price: 200},
            {size_id: 2, name: '5x3', description: '5 inches diameter, 3 inches height', base_price: 300},
            {size_id: 3, name: '6x3', description: '6 inches diameter, 3 inches height', base_price: 400}
        ];
        renderSizes(mockSizes);
    }
}

function renderSizes(sizes) {
    const container = document.getElementById('sizeOptions');
    container.innerHTML = '';
    
    sizes.forEach(size => {
        const col = document.createElement('div');
        col.className = 'col-md-4';
        col.innerHTML = `
            <div class="size-option" data-size="${size.name}" data-price="${size.base_price}" data-id="${size.size_id}">
                <h5>${size.name}</h5>
                <p class="mb-0">Base: <strong>₱${parseFloat(size.base_price).toFixed(2)}</strong></p>
            </div>
        `;
        container.appendChild(col);
    });
    
    // Setup click listeners after rendering
    setupSizeSelection();
}

async function loadFlavors() {
    try {
        // TODO: Replace with actual API call
        const response = await fetch('/api/flavors');
        const flavors = await response.json();
        
        const select = document.getElementById('flavorSelect');
        flavors.forEach(flavor => {
            const option = document.createElement('option');
            option.value = flavor.flavor_id;
            option.textContent = `${flavor.name} (₱${flavor.price_per_layer}/layer)`;
            option.dataset.price = flavor.price_per_layer;
            select.appendChild(option);
        });
    } catch (error) {
        console.log('Using mock data for flavors');
        // Mock data
        const mockFlavors = [
            {flavor_id: 1, name: 'Chocolate', price_per_layer: 30},
            {flavor_id: 2, name: 'Vanilla', price_per_layer: 40},
            {flavor_id: 3, name: 'Strawberry', price_per_layer: 55},
            {flavor_id: 4, name: 'Ube', price_per_layer: 45},
            {flavor_id: 5, name: 'Mocha', price_per_layer: 35}
        ];
        
        const select = document.getElementById('flavorSelect');
        mockFlavors.forEach(flavor => {
            const option = document.createElement('option');
            option.value = flavor.flavor_id;
            option.textContent = `${flavor.name} (₱${flavor.price_per_layer}/layer)`;
            option.dataset.price = flavor.price_per_layer;
            select.appendChild(option);
        });
    }
}

async function loadToppings() {
    try {
        // TODO: Replace with actual API call
        const response = await fetch('/api/toppings');
        const toppings = await response.json();
        
        renderToppings(toppings);
    } catch (error) {
        console.log('Using mock data for toppings');
        // Mock data
        const mockToppings = [
            {topping_id: 1, name: 'Cherry', price: 20},
            {topping_id: 2, name: 'Chocolate Chips', price: 15},
            {topping_id: 3, name: 'Strawberry', price: 25},
            {topping_id: 4, name: 'Sprinkles', price: 10}
        ];
        
        renderToppings(mockToppings);
    }
}

function renderToppings(toppings) {
    const container = document.getElementById('toppingsList');
    container.innerHTML = '';
    
    toppings.forEach(topping => {
        const div = document.createElement('div');
        div.className = 'topping-item row align-items-center mb-2';
        div.innerHTML = `
            <div class="col-md-6">
                <strong>${topping.name}</strong>
                <span class="text-muted ms-2">(₱${topping.price} each)</span>
            </div>
            <div class="col-md-6">
                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-outline-secondary topping-btn-minus"
                            data-id="${topping.topping_id}"
                            data-name="${topping.name}"
                            data-price="${topping.price}">−</button>
                    <span class="btn btn-outline-secondary topping-quantity-display" 
                          id="topping-qty-${topping.topping_id}">0</span>
                    <button type="button" class="btn btn-outline-secondary topping-btn-plus"
                            data-id="${topping.topping_id}"
                            data-name="${topping.name}"
                            data-price="${topping.price}">+</button>
                </div>
            </div>
        `;
        container.appendChild(div);
    });
    
    // Add event listeners to +/- buttons
    document.querySelectorAll('.topping-btn-minus').forEach(btn => {
        btn.addEventListener('click', function() {
            const id = parseInt(this.dataset.id);
            const name = this.dataset.name;
            const price = parseFloat(this.dataset.price);
            adjustTopping(id, name, price, -1);
        });
    });
    
    document.querySelectorAll('.topping-btn-plus').forEach(btn => {
        btn.addEventListener('click', function() {
            const id = parseInt(this.dataset.id);
            const name = this.dataset.name;
            const price = parseFloat(this.dataset.price);
            adjustTopping(id, name, price, 1);
        });
    });
}

function adjustTopping(id, name, price, change) {
    // Find existing topping in state
    let topping = calculatorState.toppings.find(t => t.id === id);
    
    if (!topping) {
        topping = {id, name, price, quantity: 0};
        calculatorState.toppings.push(topping);
    }
    
    // Adjust quantity (min 0, max 10)
    topping.quantity = Math.max(0, Math.min(10, topping.quantity + change));
    
    // Remove topping if quantity is 0
    if (topping.quantity === 0) {
        calculatorState.toppings = calculatorState.toppings.filter(t => t.id !== id);
    }
    
    // Update display
    document.getElementById(`topping-qty-${id}`).textContent = topping.quantity;
    
    // Update price
    updatePrice();
}

// Icing colors and rendering removed - now using Light/Medium/Dark shades only

// ========================================
// Event Handlers
// ========================================

function setupSizeSelection() {
    document.querySelectorAll('.size-option').forEach(option => {
        option.addEventListener('click', function() {
            // Remove selected class from all
            document.querySelectorAll('.size-option').forEach(o => o.classList.remove('selected'));
            // Add to clicked
            this.classList.add('selected');
            
            calculatorState.size = this.dataset.size;
            calculatorState.basePrice = parseFloat(this.dataset.price);
            
            updatePrice();
        });
    });
}

function setupLayerSelection() {
    const slider = document.getElementById('layerSlider');
    const layerCount = document.getElementById('layerCount');
    
    slider.addEventListener('input', function() {
        calculatorState.numLayers = parseInt(this.value);
        layerCount.textContent = this.value;
        updatePrice();
    });
}

function setupFlavorSelection() {
    const select = document.getElementById('flavorSelect');
    
    select.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        calculatorState.flavorId = parseInt(this.value);
        calculatorState.flavorPricePerLayer = parseFloat(selectedOption.dataset.price || 0);
        updatePrice();
    });
}

// updateToppings function removed - now using adjustTopping with +/- buttons

// Save estimate functionality removed

// ========================================
// Price Calculation
// ========================================

function updatePrice() {
    const base = calculatorState.basePrice;
    
    // Layer cost: 20% of base price per layer above 1
    const layerCost = base * 0.20 * (calculatorState.numLayers - 1);
    
    // Flavor cost: separate from layers
    const flavorCost = calculatorState.flavorPricePerLayer || 0;
    
    // Toppings
    const toppingsCost = calculatorState.toppings.reduce((sum, t) => sum + (t.price * t.quantity), 0);
    
    const total = base + layerCost + flavorCost + toppingsCost;
    
    // Update UI
    document.getElementById('priceBase').textContent = formatPrice(base);
    document.getElementById('priceLayers').textContent = formatPrice(layerCost);
    document.getElementById('priceFlavor').textContent = formatPrice(flavorCost);
    document.getElementById('priceToppings').textContent = formatPrice(toppingsCost);
    document.getElementById('priceTotal').textContent = formatPrice(total);
    document.getElementById('totalPrice').textContent = formatPrice(total);
}

function formatPrice(price) {
    return '₱' + parseFloat(price).toFixed(2);
}

// ========================================
// Save Estimate
// ========================================

async function saveEstimate() {
    // Validate
    if (!calculatorState.size) {
        showNotification('Please select a cake size', 'danger');
        return;
    }
    
    if (!calculatorState.flavorId) {
        showNotification('Please select a flavor', 'danger');
        return;
    }
    
    // Validate base icing (required)
    if (!calculatorState.icing.base) {
        showNotification('Please select a shade for the Base icing (required)', 'danger');
        return;
    }
    
    const estimateData = {
        size: calculatorState.size,
        num_layers: calculatorState.numLayers,
        flavor_id: calculatorState.flavorId,
        toppings: calculatorState.toppings,
        icing: calculatorState.icing,
        total_price: parseFloat(document.getElementById('priceTotal').textContent.replace('₱', ''))
    };
    
    try {
        // TODO: Replace with actual API call
        const response = await fetch('/api/estimates', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(estimateData)
        });
        
        if (response.ok) {
            showNotification('Price estimate saved successfully! 🎉', 'success');
            // Optionally reset form
        } else {
            throw new Error('Failed to save estimate');
        }
    } catch (error) {
        console.log('Mock save:', estimateData);
        showNotification('Price estimate saved successfully! 🎉', 'success');
    }
}

// ========================================
// Utility Functions
// ========================================

function showNotification(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container-fluid');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto dismiss after 3 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}
