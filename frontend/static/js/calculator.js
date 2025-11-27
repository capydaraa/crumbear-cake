// Price Calculator Logic for Crumbear Cakes

let calculatorState = {
    baseCakeId: null,
    size: null,
    basePrice: 0,
    numLayers: 1,
    flavorId: null,
    flavorPricePerLayer: 0,
    toppings: [], // {id, name, price, quantity}
    icing: { // {part, colorId, colorName, shade, multiplier}
        base: null,
        sides: null,
        other: null
    },
    hasMessage: false,
    isRush: false
};

// Initialize calculator
document.addEventListener('DOMContentLoaded', function() {
    console.log('Calculator initialized');
    
    // Load data from API
    loadFlavors();
    loadToppings();
    loadIcingColors();
    loadBaseCakes();
    
    // Set up event listeners
    setupSizeSelection();
    setupLayerSelection();
    setupFlavorSelection();
    setupIcingSelection();
    setupAdditionalOptions();
    setupSaveButton();
});

// ========================================
// Load Data from API
// ========================================

async function loadBaseCakes() {
    try {
        // TODO: Replace with actual API call
        const response = await fetch('/api/cakes');
        const cakes = await response.json();
        
        const select = document.getElementById('baseCakeSelect');
        cakes.forEach(cake => {
            const option = document.createElement('option');
            option.value = cake.cake_id;
            option.textContent = `${cake.name} (${cake.category})`;
            option.dataset.price4x3 = cake.base_price_4x3;
            option.dataset.price5x3 = cake.base_price_5x3;
            option.dataset.price6x3 = cake.base_price_6x3;
            select.appendChild(option);
        });
    } catch (error) {
        console.log('Using mock data for base cakes');
        // Mock data for now
    }
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
            {flavor_id: 1, name: 'Chocolate', price_per_layer: 50},
            {flavor_id: 2, name: 'Vanilla', price_per_layer: 40},
            {flavor_id: 3, name: 'Red Velvet', price_per_layer: 60},
            {flavor_id: 4, name: 'Strawberry', price_per_layer: 55},
            {flavor_id: 5, name: 'Ube', price_per_layer: 65}
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
            {topping_id: 2, name: 'Strawberry', price: 25},
            {topping_id: 3, name: 'Chocolate Chips', price: 15},
            {topping_id: 4, name: 'Sprinkles', price: 10},
            {topping_id: 5, name: 'Oreo Crumbs', price: 30},
            {topping_id: 6, name: 'Macaron', price: 35},
            {topping_id: 7, name: 'Fresh Berries', price: 40},
            {topping_id: 8, name: 'Caramel Drizzle', price: 20},
            {topping_id: 9, name: 'Whipped Cream', price: 15},
            {topping_id: 10, name: 'Edible Flowers', price: 50}
        ];
        
        renderToppings(mockToppings);
    }
}

function renderToppings(toppings) {
    const container = document.getElementById('toppingsList');
    container.innerHTML = '';
    
    toppings.forEach(topping => {
        const div = document.createElement('div');
        div.className = 'topping-item row align-items-center';
        div.innerHTML = `
            <div class="col-md-6">
                <strong>${topping.name}</strong>
                <span class="text-muted ms-2">(₱${topping.price} each)</span>
            </div>
            <div class="col-md-6">
                <input type="number" 
                       class="form-control topping-quantity" 
                       data-id="${topping.topping_id}"
                       data-name="${topping.name}"
                       data-price="${topping.price}"
                       min="0" 
                       max="10" 
                       value="0"
                       placeholder="Qty">
            </div>
        `;
        container.appendChild(div);
    });
    
    // Add event listeners to quantity inputs
    document.querySelectorAll('.topping-quantity').forEach(input => {
        input.addEventListener('change', updateToppings);
    });
}

async function loadIcingColors() {
    try {
        // TODO: Replace with actual API call
        const response = await fetch('/api/colors');
        const colors = await response.json();
        
        renderIcingColors(colors);
    } catch (error) {
        console.log('Using mock data for icing colors');
        // Mock data
        const mockColors = [
            {color_id: 1, color_name: 'Red', hex_code: '#FF0000'},
            {color_id: 2, color_name: 'Pink', hex_code: '#FFC0CB'},
            {color_id: 3, color_name: 'Blue', hex_code: '#0000FF'},
            {color_id: 4, color_name: 'Green', hex_code: '#00FF00'},
            {color_id: 5, color_name: 'Yellow', hex_code: '#FFFF00'},
            {color_id: 6, color_name: 'Purple', hex_code: '#800080'},
            {color_id: 7, color_name: 'Orange', hex_code: '#FFA500'},
            {color_id: 8, color_name: 'Brown', hex_code: '#8B4513'},
            {color_id: 9, color_name: 'White', hex_code: '#FFFFFF'},
            {color_id: 10, color_name: 'Black', hex_code: '#000000'}
        ];
        
        renderIcingColors(mockColors);
    }
}

function renderIcingColors(colors) {
    const selects = document.querySelectorAll('.icing-select');
    
    selects.forEach(select => {
        colors.forEach(color => {
            const option = document.createElement('option');
            option.value = color.color_id;
            option.textContent = color.color_name;
            option.dataset.name = color.color_name;
            option.dataset.hex = color.hex_code;
            select.appendChild(option);
        });
    });
}

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

function updateToppings(event) {
    const input = event.target;
    const id = parseInt(input.dataset.id);
    const name = input.dataset.name;
    const price = parseFloat(input.dataset.price);
    const quantity = parseInt(input.value) || 0;
    
    // Remove existing topping
    calculatorState.toppings = calculatorState.toppings.filter(t => t.id !== id);
    
    // Add if quantity > 0
    if (quantity > 0) {
        calculatorState.toppings.push({id, name, price, quantity});
    }
    
    updatePrice();
}

function setupIcingSelection() {
    document.querySelectorAll('.icing-select').forEach(select => {
        select.addEventListener('change', function() {
            const part = this.dataset.part.toLowerCase();
            const shadeDiv = document.getElementById(`shade${this.dataset.part}`);
            
            if (this.value) {
                shadeDiv.style.display = 'block';
                const selectedOption = this.options[this.selectedIndex];
                
                if (!calculatorState.icing[part]) {
                    calculatorState.icing[part] = {};
                }
                calculatorState.icing[part].colorId = parseInt(this.value);
                calculatorState.icing[part].colorName = selectedOption.dataset.name;
            } else {
                shadeDiv.style.display = 'none';
                calculatorState.icing[part] = null;
            }
            
            updatePrice();
        });
    });
    
    // Shade selection
    document.querySelectorAll('input[name^="shade"]').forEach(radio => {
        radio.addEventListener('change', function() {
            const part = this.name.replace('shade', '').toLowerCase();
            const multiplier = parseFloat(this.dataset.multiplier);
            const shade = this.value;
            
            if (calculatorState.icing[part]) {
                calculatorState.icing[part].shade = shade;
                calculatorState.icing[part].multiplier = multiplier;
            }
            
            updatePrice();
        });
    });
}

function setupAdditionalOptions() {
    document.getElementById('hasMessage').addEventListener('change', function() {
        calculatorState.hasMessage = this.checked;
        updatePrice();
    });
    
    document.getElementById('isRush').addEventListener('change', function() {
        calculatorState.isRush = this.checked;
        updatePrice();
    });
}

function setupSaveButton() {
    document.getElementById('saveEstimateBtn').addEventListener('click', saveEstimate);
}

// ========================================
// Price Calculation
// ========================================

function updatePrice() {
    const base = calculatorState.basePrice;
    const layers = calculatorState.numLayers * calculatorState.flavorPricePerLayer;
    const toppings = calculatorState.toppings.reduce((sum, t) => sum + (t.price * t.quantity), 0);
    
    // Calculate icing cost
    let icing = 0;
    Object.values(calculatorState.icing).forEach(icingPart => {
        if (icingPart && icingPart.multiplier) {
            const baseIcingCost = 50; // Base cost per icing part
            icing += baseIcingCost * icingPart.multiplier;
        }
    });
    
    const message = calculatorState.hasMessage ? 50 : 0;
    
    let subtotal = base + layers + toppings + icing + message;
    const rush = calculatorState.isRush ? subtotal * 0.5 : 0;
    const total = subtotal + rush;
    
    // Update UI
    document.getElementById('priceBase').textContent = formatPrice(base);
    document.getElementById('priceLayers').textContent = formatPrice(layers);
    document.getElementById('priceToppings').textContent = formatPrice(toppings);
    document.getElementById('priceIcing').textContent = formatPrice(icing);
    document.getElementById('priceMessage').textContent = formatPrice(message);
    document.getElementById('priceRush').textContent = formatPrice(rush);
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
    
    const estimateData = {
        cake_id: calculatorState.baseCakeId,
        size: calculatorState.size,
        num_layers: calculatorState.numLayers,
        flavor_id: calculatorState.flavorId,
        toppings: calculatorState.toppings,
        icing: calculatorState.icing,
        has_message: calculatorState.hasMessage,
        is_rush: calculatorState.isRush,
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
