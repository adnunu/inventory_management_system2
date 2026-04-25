from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# In-memory database (array storage)
inventory = [
    {"id": 1, "name": "Apple Juice", "barcode": "1234567890123", "price": 4.99, "quantity": 50, "brand": "Organic Farms"},
    {"id": 2, "name": "Wheat Bread", "barcode": "2345678901234", "price": 3.49, "quantity": 30, "brand": "Baker's Best"}
]
next_id = 3

def find_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None

# ============ CRUD OPERATIONS ============

@app.route('/api/inventory', methods=['GET'])
def get_all_items():
    """READ - Get all inventory items"""
    return jsonify({"success": True, "data": inventory, "count": len(inventory)})

@app.route('/api/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """READ - Get single inventory item"""
    item = find_item(item_id)
    if item:
        return jsonify({"success": True, "data": item})
    return jsonify({"success": False, "error": "Item not found"}), 404

@app.route('/api/inventory', methods=['POST'])
def create_item():
    """CREATE - Add new inventory item"""
    data = request.get_json()
    global next_id
    
    new_item = {
        "id": next_id,
        "name": data.get('name'),
        "barcode": data.get('barcode', ''),
        "price": float(data.get('price')),
        "quantity": int(data.get('quantity')),
        "brand": data.get('brand', '')
    }
    
    inventory.append(new_item)
    next_id += 1
    return jsonify({"success": True, "data": new_item}), 201

@app.route('/api/inventory/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """UPDATE (Full) - Replace entire item"""
    item = find_item(item_id)
    if not item:
        return jsonify({"success": False, "error": "Item not found"}), 404
    
    data = request.get_json()
    item['name'] = data.get('name', item['name'])
    item['barcode'] = data.get('barcode', item['barcode'])
    item['price'] = float(data.get('price', item['price']))
    item['quantity'] = int(data.get('quantity', item['quantity']))
    item['brand'] = data.get('brand', item['brand'])
    
    return jsonify({"success": True, "data": item})

@app.route('/api/inventory/<int:item_id>', methods=['PATCH'])
def patch_item(item_id):
    """UPDATE (Partial) - Update specific fields"""
    item = find_item(item_id)
    if not item:
        return jsonify({"success": False, "error": "Item not found"}), 404
    
    data = request.get_json()
    if 'name' in data:
        item['name'] = data['name']
    if 'price' in data:
        item['price'] = float(data['price'])
    if 'quantity' in data:
        item['quantity'] = int(data['quantity'])
    
    return jsonify({"success": True, "data": item})

@app.route('/api/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """DELETE - Remove item from inventory"""
    global inventory
    item = find_item(item_id)
    if not item:
        return jsonify({"success": False, "error": "Item not found"}), 404
    
    inventory = [i for i in inventory if i["id"] != item_id]
    return jsonify({"success": True, "message": "Item deleted successfully"})

# ============ EXTERNAL API INTEGRATION ============

@app.route('/api/fetch-product/<barcode>', methods=['GET'])
def fetch_product(barcode):
    """Fetch product from OpenFoodFacts API"""
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    
    try:
        response = requests.get(url, headers={'User-Agent': 'InventoryApp/1.0'})
        data = response.json()
        
        if data.get('status') == 1:
            product = data['product']
            return jsonify({
                "success": True,
                "barcode": barcode,
                "name": product.get('product_name', 'Unknown'),
                "brand": product.get('brands', 'Unknown'),
                "category": product.get('categories', 'Unknown')
            })
        return jsonify({"success": False, "error": "Product not found"}), 404
    except:
        return jsonify({"success": False, "error": "API request failed"}), 500

@app.route('/api/search-product', methods=['GET'])
def search_product():
    """Search products by name using OpenFoodFacts"""
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query parameter 'q' required"}), 400
    
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&search_simple=1&json=1&page_size=5"
    
    try:
        response = requests.get(url, headers={'User-Agent': 'InventoryApp/1.0'})
        data = response.json()
        
        results = []
        for product in data.get('products', []):
            results.append({
                "name": product.get('product_name', 'Unknown'),
                "barcode": product.get('code', ''),
                "brand": product.get('brands', 'Unknown')
            })
        
        return jsonify({"success": True, "data": results})
    except:
        return jsonify({"success": False, "error": "Search failed"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "inventory_count": len(inventory)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)