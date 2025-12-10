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
        role = "admin" if type(self).__name__.lower() == "admin" else "cashier"
        self.role = role

    def save_user(self):
        user_record = {
            'username' : self.username,
            'password' : self.__password,
            'role' : self.role,
            'created_at' : str(datetime.datetime.now())
        }

        path = "billing/users.json"

        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError: # If file is empty or corrupted
                data = []
        else:
            data = []

        data.append(user_record)

        with open(path, 'w') as f:
            json.dump(data, f, indent=4) # indent to make it clear

    @staticmethod
    def login(username, password):
        path = "billing/users.json"

        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError: # If file is empty or corrupted
                data = []
        else:
            data = []

        for u in data:
            if u["username"].lower() == str(username).lower():
                if u["password"] != str(password):
                    print("*"*15 + "Incorrect password" + "*"*15)
                    return None

                role = u["role"]

                if role == "admin":
                    return Admin(u["username"], u["password"])
                else:
                    return Cashier(u["username"], u["password"])
        else:
            print("*"*15 + f"{username} not registered" + "*"*15)
            return None

class Admin(Cashier):
    def __init__(self, username, password):
        super().__init__(username, password)

    def view_inventory(self):
        Product.view_inventory(self)

    def add_product(self, name, quantity, price):
        product = Product(name, quantity, price)
        return product

    def update_product(self, product_id, **kwargs):
        Product.product_update(self, product_id, **kwargs)
    
    def delete_product(self, product_id):
        Product.product_delete(self, product_id)