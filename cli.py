import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

def print_menu():
    print("\n" + "="*60)
    print(" INVENTORY MANAGEMENT SYSTEM")
    print("="*60)
    print("1. View all items")
    print("2. View single item by ID")
    print("3. Add new item")
    print("4. Update item (full update)")
    print("5. Update item (partial update)")
    print("6. Delete item")
    print("7. Fetch product from OpenFoodFacts API (by barcode)")
    print("8. Search products by name (API)")
    print("0. Exit")
    print("-"*60)

def view_all():
    try:
        response = requests.get(f"{BASE_URL}/inventory")
        data = response.json()
        
        if data.get('success'):
            items = data['data']
            if items:
                print("\n" + "-"*80)
                for item in items:
                    print(f"ID: {item['id']} | {item['name']} | ${item['price']} | Qty: {item['quantity']} | Brand: {item['brand']}")
                print("-"*80)
                print(f"Total items: {data['count']}")
            else:
                print("\nNo items in inventory.")
        else:
            print(f"\nError: {data.get('error')}")
    except Exception as e:
        print(f"\nError: Cannot connect to server. Make sure Flask is running.")

def view_single():
    try:
        item_id = input("Enter item ID: ")
        response = requests.get(f"{BASE_URL}/inventory/{item_id}")
        data = response.json()
        
        if data.get('success'):
            item = data['data']
            print("\n" + "-"*40)
            for key, value in item.items():
                print(f"{key.upper()}: {value}")
            print("-"*40)
        else:
            print(f"\nError: {data.get('error')}")
    except Exception as e:
        print(f"\nError: {str(e)}")

def add_item():
    try:
        print("\n--- ADD NEW ITEM ---")
        name = input("Product name: ")
        price = float(input("Price: $"))
        quantity = int(input("Quantity: "))
        brand = input("Brand: ")
        barcode = input("Barcode (optional): ")
        
        item_data = {
            "name": name,
            "price": price,
            "quantity": quantity,
            "brand": brand,
            "barcode": barcode
        }
        
        response = requests.post(f"{BASE_URL}/inventory", json=item_data)
        data = response.json()
        
        if data.get('success'):
            print(f"\n✓ Item added successfully! (ID: {data['data']['id']})")
        else:
            print(f"\nError: {data.get('error')}")
    except Exception as e:
        print(f"\nError: {str(e)}")

def update_item_full():
    try:
        item_id = input("Enter item ID to update: ")
        
        # Get current item
        response = requests.get(f"{BASE_URL}/inventory/{item_id}")
        if not response.json().get('success'):
            print("Item not found!")
            return
        
        print("\n--- ENTER NEW VALUES ---")
        name = input("Name: ")
        price = float(input("Price: $"))
        quantity = int(input("Quantity: "))
        brand = input("Brand: ")
        
        update_data = {
            "name": name,
            "price": price,
            "quantity": quantity,
            "brand": brand
        }
        
        response = requests.put(f"{BASE_URL}/inventory/{item_id}", json=update_data)
        if response.json().get('success'):
            print("\n✓ Item updated successfully!")
        else:
            print("\nError: Update failed")
    except Exception as e:
        print(f"\nError: {str(e)}")

def update_item_partial():
    try:
        item_id = input("Enter item ID to update: ")
        
        response = requests.get(f"{BASE_URL}/inventory/{item_id}")
        if not response.json().get('success'):
            print("Item not found!")
            return
        
        print("\n--- ENTER VALUES TO UPDATE (press Enter to skip) ---")
        name = input("New name: ")
        price = input("New price: $")
        quantity = input("New quantity: ")
        
        update_data = {}
        if name:
            update_data['name'] = name
        if price:
            update_data['price'] = float(price)
        if quantity:
            update_data['quantity'] = int(quantity)
        
        if update_data:
            response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=update_data)
            if response.json().get('success'):
                print("\n✓ Item updated successfully!")
            else:
                print("\nError: Update failed")
        else:
            print("\nNo updates provided.")
    except Exception as e:
        print(f"\nError: {str(e)}")

def delete_item():
    try:
        item_id = input("Enter item ID to delete: ")
        confirm = input(f"Are you sure you want to delete item {item_id}? (y/N): ")
        
        if confirm.lower() == 'y':
            response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
            if response.json().get('success'):
                print("\n✓ Item deleted successfully!")
            else:
                print("\nError: Item not found")
    except Exception as e:
        print(f"\nError: {str(e)}")

def fetch_from_api():
    try:
        barcode = input("Enter product barcode: ")
        response = requests.get(f"{BASE_URL}/fetch-product/{barcode}")
        data = response.json()
        
        if data.get('success'):
            print("\n--- PRODUCT FROM OPENFOODFACTS ---")
            print(f"Name: {data['name']}")
            print(f"Brand: {data['brand']}")
            print(f"Category: {data['category']}")
            print(f"Barcode: {data['barcode']}")
        else:
            print(f"\nError: {data.get('error')}")
    except Exception as e:
        print(f"\nError: {str(e)}")

def search_api():
    try:
        query = input("Enter product name to search: ")
        response = requests.get(f"{BASE_URL}/search-product", params={'q': query})
        data = response.json()
        
        if data.get('success'):
            products = data['data']
            if products:
                print(f"\n--- FOUND {len(products)} PRODUCTS ---")
                for i, product in enumerate(products, 1):
                    print(f"{i}. {product['name']}")
                    print(f"   Brand: {product['brand']}")
                    print(f"   Barcode: {product['barcode']}\n")
            else:
                print("\nNo products found.")
        else:
            print(f"\nError: {data.get('error')}")
    except Exception as e:
        print(f"\nError: {str(e)}")

def main():
    print("\n" + "="*60)
    print(" WELCOME TO INVENTORY MANAGEMENT SYSTEM")
    print("="*60)
    print("\nMake sure the Flask server is running: python3 app.py\n")
    
    while True:
        print_menu()
        choice = input("\nEnter your choice: ")
        
        if choice == '0':
            print("\nGoodbye! ")
            break
        elif choice == '1':
            view_all()
        elif choice == '2':
            view_single()
        elif choice == '3':
            add_item()
        elif choice == '4':
            update_item_full()
        elif choice == '5':
            update_item_partial()
        elif choice == '6':
            delete_item()
        elif choice == '7':
            fetch_from_api()
        elif choice == '8':
            search_api()
        else:
            print("\nInvalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()