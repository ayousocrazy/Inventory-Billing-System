import json
import os
import time
import datetime
from product import *

os.chdir(r"C:\Users\HP\Desktop\Project\Inventory and Billing Management System")

class Cashier:
    def __init__(self, username, password):
        self.username = str(username)
        self.__password = str(password)

        # Assign role based on class type
        self.role = "admin" if type(self).__name__.lower() == "admin" else "cashier"
        
    @staticmethod
    def _load_users():
        path = "billing/users.json"
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    @staticmethod
    def login(username, password):
        users = Cashier._load_users()

        for u in users:
            if u["username"].lower() == str(username).lower():
                if u["password"] != str(password):
                    print("~"*5 + " Incorrect password " + "*"*5)
                    return None

                return Admin(u["username"], u["password"]) if u["role"] == "admin" else Cashier(u["username"], u["password"])

        print("~"*5 + f"{username} not registered" + "~"*5)
        return None

class Admin(Cashier):
    def view_inventory(self):
        Product.view_inventory(self)

    def add_product(self, name, quantity, price):
        return Product(name, quantity, price)

    def update_product(self, product_id, **kwargs):
        Product.product_update(self, product_id, **kwargs)
    
    def delete_product(self, product_id):
        Product.product_delete(self, product_id)

    def view_report(self, option):
        if option in ["1", "(1)"]:
            self._view_sales_report()
        elif option in ["2", "(2)"]:
            self._view_low_stock_report()
        else:
            print("~" * 15 + "Option not found" + "~" * 15)

    def _view_sales_report(self):
        # Show sales report
        path = "billing/sales.json"
        reports = []
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    reports = json.load(f)
            except json.JSONDecodeError:
                pass

        print("\nSales Report")
        print("_" * 12)

        if not reports:
            print("~" * 5 + " No Sales Yet " + "~" * 5)
            return

        print("_" * 50)
        print("| Date | Product Sold |")
        for r in reports:
            print(f"| {r['date']} | ", end="")
            for p in r["product_list"]:
                print(f"({p['product_id']},{p['quantity']})", end=" ")
            print("|\n" + "-" * 50)
        print("_" * 50)

    def _view_low_stock_report(self):
        # Show products with stock <= 10
        path = "billing/products.json"
        products = []
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    products = json.load(f)
            except json.JSONDecodeError:
                pass

        print("\nInventory Report")
        print("_" * 16)

        low_stock = [p for p in products if p["stock"] <= 10]
        if not low_stock:
            print("(All stocks are sufficient)")
        else:
            for p in low_stock:
                print(f"| {p['product_id']} | Only {p['stock']} left")
            print("_" * 50)
        
    def save_user(self, username, password, role):
        user_record = {
            'username' : username,
            'password' : password,
            'role' : role,
            'created_at' : str(datetime.datetime.now())
        }

        path = "billing/users.json"

        users = []
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    users = json.load(f)
            except json.JSONDecodeError: # If file is empty or corrupted
                pass

        users.append(user_record)

        with open(path, 'w') as f:
            json.dump(users, f, indent=4) # indent to make it clear
        print(f"User '{username}' created successfully!")