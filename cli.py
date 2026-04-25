import requests

BASE = "http://127.0.0.1:5000"

def menu():
    print("\n" + "="*40)
    print("INVENTORY SYSTEM")
    print("="*40)
    print("1. View all items")
    print("2. Add item")
    print("3. Update item")
    print("4. Delete item")
    print("5. Fetch product from API")
    print("0. Exit")

def view_all():
    r = requests.get(f"{BASE}/inventory")
    items = r.json()
    print("\nItems:")
    for i in items:
        print(f"ID:{i['id']} | {i['name']} | ${i['price']} | Qty:{i['quantity']}")

def add_item():
    name = input("Name: ")
    price = float(input("Price: "))
    qty = int(input("Quantity: "))
    r = requests.post(f"{BASE}/inventory", json={"name": name, "price": price, "quantity": qty})
    if r.status_code == 201:
        print("Added!")

def update_item():
    id = int(input("Item ID: "))
    price = input("New price (Enter to skip): ")
    qty = input("New quantity (Enter to skip): ")
    data = {}
    if price:
        data['price'] = float(price)
    if qty:
        data['quantity'] = int(qty)
    if data:
        r = requests.put(f"{BASE}/inventory/{id}", json=data)
        if r.status_code == 200:
            print("Updated!")

def delete_item():
    id = int(input("Item ID: "))
    r = requests.delete(f"{BASE}/inventory/{id}")
    if r.status_code == 200:
        print("Deleted!")

def fetch_api():
    barcode = input("Enter barcode: ")
    r = requests.get(f"{BASE}/fetch/{barcode}")
    if r.status_code == 200:
        data = r.json()
        print(f"\nProduct: {data.get('name')}")
        print(f"Brand: {data.get('brand')}")
    else:
        print("Not found")

def main():
    print("Make sure server is running: python app.py")
    while True:
        menu()
        choice = input("Choice: ")
        if choice == '1':
            view_all()
        elif choice == '2':
            add_item()
        elif choice == '3':
            update_item()
        elif choice == '4':
            delete_item()
        elif choice == '5':
            fetch_api()
        elif choice == '0':
            print("Bye!")
            break
        input("\nPress Enter...")

if __name__ == "__main__":
    main()