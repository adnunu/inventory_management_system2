from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Inventory database (array)
inventory = [
    {"id": 1, "name": "Apple Juice", "price": 4.99, "quantity": 50},
    {"id": 2, "name": "Wheat Bread", "price": 3.49, "quantity": 30}
]
next_id = 3

# CRUD OPERATIONS
@app.route('/inventory', methods=['GET'])
def get_all():
    return jsonify(inventory)

@app.route('/inventory/<int:id>', methods=['GET'])
def get_one(id):
    for item in inventory:
        if item['id'] == id:
            return jsonify(item)
    return jsonify({"error": "Not found"}), 404

@app.route('/inventory', methods=['POST'])
def create():
    global next_id
    data = request.get_json()
    item = {"id": next_id, "name": data['name'], "price": data['price'], "quantity": data['quantity']}
    inventory.append(item)
    next_id += 1
    return jsonify(item), 201

@app.route('/inventory/<int:id>', methods=['PUT'])
def update(id):
    for item in inventory:
        if item['id'] == id:
            data = request.get_json()
            item.update(data)
            return jsonify(item)
    return jsonify({"error": "Not found"}), 404

@app.route('/inventory/<int:id>', methods=['DELETE'])
def delete(id):
    global inventory
    for i, item in enumerate(inventory):
        if item['id'] == id:
            inventory.pop(i)
            return jsonify({"message": "Deleted"})
    return jsonify({"error": "Not found"}), 404

# EXTERNAL API
@app.route('/fetch/<barcode>', methods=['GET'])
def fetch(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        r = requests.get(url, headers={'User-Agent': 'MyApp/1.0'})
        data = r.json()
        if data.get('status') == 1:
            p = data['product']
            return jsonify({"name": p.get('product_name'), "brand": p.get('brands')})
        return jsonify({"error": "Not found"}), 404
    except:
        return jsonify({"error": "API error"}), 500

if __name__ == '__main__':
    app.run(debug=True)