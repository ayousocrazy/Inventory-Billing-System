import json
import os
import time
import datetime

BASE_DIR = r"C:\Users\HP\Desktop\Project\Inventory and Billing Management System"

PRODUCT_FILE = os.path.join(BASE_DIR, "billing/products.json")
SALES_FILE = os.path.join(BASE_DIR, "billing/sales.json")
DELETED_FILE = os.path.join(BASE_DIR, "billing/deleted.json")
BILLS_DIR = os.path.join(BASE_DIR, "billing/bills")

os.makedirs(BILLS_DIR, exist_ok=True)

def load_json(path, default=None):
    if not os.path.exists(path):
        return default if default is not None else []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default if default is not None else []


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def is_admin(user):
    return type(user).__name__.lower() == "admin"



class Product:
    def __init__(self, name, stock, price):
        self.name = name
        self.stock = int(stock)
        self.price = float(price)

        data = Product._load_all()
        num = len(data) + 1
        t = time.strftime("%y%m")

        self.product_id = f"{t}-{num}-{self.name[0].upper()}"
        self._save()

    @staticmethod
    def _load_all():
        return load_json(PRODUCT_FILE, [])

    def _save(self):
        data = Product._load_all()
        data.append({
            "product_id": self.product_id,
            "name": self.name,
            "stock": self.stock,
            "price": self.price
        })
        save_json(PRODUCT_FILE, data)

    @staticmethod
    def view_products():
        data = Product._load_all()
        if not data:
            print("Stock Empty")
            return

        print("\n| Product ID | Product Name | Stock |")
        for p in data:
            print(f"| {p['product_id']} | {p['name']} | {p['stock']} |")

    @staticmethod
    def view_inventory(user):
        if not is_admin(user):
            print("~~~~~ Access Denied ~~~~~")
            return

        data = Product._load_all()
        if not data:
            print("~~~~~ Stock Empty ~~~~~")
            return

        total = 0
        print("\n| ID | Name | Stock | Price |")
        for p in data:
            total += p["stock"] * p["price"]
            print(f"| {p['product_id']} | {p['name']} | {p['stock']} | {p['price']} |")

        print("_" * 30)
        print("Total Inventory:", total)

    @staticmethod
    def product_update(user, product_id, **kwargs):
        if not is_admin(user):
            print("~~~~~ Access Denied ~~~~~")
            return

        data = Product._load_all()
        for p in data:
            if p["product_id"] == product_id:
                p["name"] = kwargs.get("n", p["name"])
                p["stock"] = int(kwargs.get("s", p["stock"]))
                p["price"] = float(kwargs.get("p", p["price"]))

                save_json(PRODUCT_FILE, data)
                print("Product updated successfully.")
                return

        print("Product not found.")

    @staticmethod
    def product_delete(user, product_id):
        if not is_admin(user):
            print("~~~~~ Access Denied ~~~~~")
            return

        data = Product._load_all()
        for p in data:
            if p["product_id"] == product_id:
                data.remove(p)
                save_json(PRODUCT_FILE, data)

                with open(DELETED_FILE, "a") as f:
                    f.write(json.dumps({
                        "deleted_product": p,
                        "deleted_at": str(datetime.datetime.now())
                    }) + "\n")

                print("Product deleted successfully.")
                return

        print("Product not found.")



class Cart:
    def __init__(self):
        self.items = []
        self.total = 0

    def add_to_cart(self, product_id, qty):
        qty = int(qty)
        products = Product._load_all()

        for p in products:
            if p["product_id"] == product_id:
                qty = min(qty, p["stock"])

                self.items.append({
                    "product_id": product_id,
                    "name": p["name"],
                    "qty": qty,
                    "price": p["price"]
                })

                self.total += qty * p["price"]
                print("Added to cart.")
                return

        print("Product not found.")

    def view_cart(self):
        if not self.items:
            print("Cart empty")
            return

        print("\n| S.N | Product | Qty | Price |")
        for i, item in enumerate(self.items, 1):
            print(f"| {i} | {item['name']} | {item['qty']} | {item['price']} |")

        print("Total:", self.total)

    def update_item(self, index, new_qty):
        if index not in range(len(self.items)):
            print("Invalid item index")
            return

        item = self.items[index]
        products = Product._load_all()

        for p in products:
            if p["product_id"] == item["product_id"]:
                if new_qty > p["stock"]:
                    print("Not enough stock")
                    return

                self.total -= item["qty"] * item["price"]
                item["qty"] = new_qty
                self.total += new_qty * item["price"]
                print("Cart updated.")
                return

    def delete_item(self, index):
        if index not in range(len(self.items)):
            print("Invalid item index")
            return

        item = self.items.pop(index)
        self.total -= item["qty"] * item["price"]
        print("Item removed.")

    def checkout(self):
        if not self.items:
            print("Cart empty")
            return

        products = Product._load_all()
        p_map = {p["product_id"]: p for p in products}

        for item in self.items:
            p_map[item["product_id"]]["stock"] -= item["qty"]

        save_json(PRODUCT_FILE, list(p_map.values()))

        bill_path = os.path.join(BILLS_DIR, f"bill-{int(time.time())}.json")
        save_json(bill_path, {
            "items": self.items,
            "total": self.total,
            "created_at": str(datetime.datetime.now())
        })

        sales = load_json(SALES_FILE, [])
        today = time.strftime("%Y-%m-%d")

        for s in sales:
            if s["date"] == today:
                s["product_list"].extend(
                    {"product_id": i["product_id"], "quantity": i["qty"]}
                    for i in self.items
                )
                break
        else:
            sales.append({
                "date": today,
                "product_list": [
                    {"product_id": i["product_id"], "quantity": i["qty"]}
                    for i in self.items
                ]
            })

        save_json(SALES_FILE, sales)

        print("Checkout complete. Bill saved:", bill_path)
        self.items.clear()
        self.total = 0