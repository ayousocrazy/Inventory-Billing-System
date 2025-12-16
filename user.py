import json
import os
import datetime
from product import Product

BASE_DIR = r"C:\Users\HP\Desktop\Project\Inventory and Billing Management System"
USERS_FILE = os.path.join(BASE_DIR, "billing/users.json")
SALES_FILE = os.path.join(BASE_DIR, "billing/sales.json")
PRODUCT_FILE = os.path.join(BASE_DIR, "billing/products.json")



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



class Cashier:
    def __init__(self, username, password, role="cashier"):
        self.username = str(username)
        self.__password = str(password)
        self.role = role

    @staticmethod
    def login(username, password):
        users = load_json(USERS_FILE, [])

        for u in users:
            if u["username"].lower() == username.lower():
                if Cashier.xor_decrypt(u["password"]) != password:
                    print("~~~~~ Incorrect password ~~~~~")
                    return None

                return Admin(u["username"], u["password"]) if u["role"] == "admin" \
                    else Cashier(u["username"], u["password"])

        print(f"~~~~~ {username} not registered ~~~~~")
        return None

    @staticmethod
    def xor_encrypt(text, key=42):
        return "".join(chr(ord(c) ^ key) for c in text)

    @staticmethod
    def xor_decrypt(text, key=42):
        return "".join(chr(ord(c) ^ key) for c in text)



class Admin(Cashier):
    def __init__(self, username, password):
        super().__init__(username, password, role="admin")

    def view_inventory(self):
        Product.view_inventory(self)

    def add_product(self, name, qty, price):
        Product(name, qty, price)

    def update_product(self, product_id, **kwargs):
        Product.product_update(self, product_id, **kwargs)

    def delete_product(self, product_id):
        Product.product_delete(self, product_id)

    def view_report(self, option):
        if option == "1":
            self._sales_report()
        elif option == "2":
            self._low_stock_report()
        else:
            print("~~~~~ Option not found ~~~~~")

    def _sales_report(self):
        reports = load_json(SALES_FILE, [])

        print("\nSales Report")
        print("-" * 40)

        if not reports:
            print("No sales yet")
            return

        for r in reports:
            print(f"Date: {r['date']}")
            for p in r["product_list"]:
                print(f"  - {p['product_id']} × {p['quantity']}")
            print("-" * 40)

    def _low_stock_report(self):
        products = load_json(PRODUCT_FILE, [])
        low = [p for p in products if p["stock"] <= 10]

        print("\nLow Stock Report")
        print("-" * 30)

        if not low:
            print("All stocks sufficient")
            return

        for p in low:
            print(f"{p['product_id']} → {p['stock']} left")

    def save_user(self, username, password, role):
        users = load_json(USERS_FILE, [])

        users.append({
            "username": username,
            "password": self.xor_encrypt(password),
            "role": role,
            "created_at": str(datetime.datetime.now())
        })

        save_json(USERS_FILE, users)
        print(f"User '{username}' created successfully")

    def view_users(self):
        users = load_json(USERS_FILE, [])

        if not users:
            print("No users found")
            return []

        print("\n| S.N | Username | Role |")
        print("-" * 30)
        for i, u in enumerate(users, 1):
            print(f"| {i} | {u['username']} | {u['role']} |")
        print("-" * 30)

        return users

    def delete_user(self, index):
        users = self.view_users()
        if not users:
            return

        if index < 0 or index >= len(users):
            print("Invalid index")
            return

        if users[index]["username"] == self.username:
            print("~~~~~ Cannot delete yourself ~~~~~")
            return

        deleted = users.pop(index)
        save_json(USERS_FILE, users)
        print(f"User '{deleted['username']}' deleted")

    def update_user(self, index, name="", password="", role=""):
        users = self.view_users()
        if not users:
            return

        if index < 0 or index >= len(users):
            print("Invalid index")
            return

        user = users[index]

        if user["username"] == self.username:
            print("~~~~~ Cannot modify yourself ~~~~~")
            return

        if name:
            user["username"] = name
        if password:
            user["password"] = self.xor_encrypt(password)
        if role:
            user["role"] = role

        save_json(USERS_FILE, users)
        print("User updated successfully")