import json
import os
import time
from product import *
os.chdir(r"C:\Users\HP\Desktop\Project\Inventory and Billing Management System")

class Cashier:
    def __init__(self, username, password):
        self.username = username
        self.__password = password
        self.created_at = time.time()
        self.save_user()

    def save_user(self):
        role = "admin" if type(self).__name__.lower() == "admin" else "cashier"

        user_record = {
            'username' : self.username,
            'password' : self.__password,
            'role' : role,
            'created_at' : self.created_at
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

class Admin(Cashier):
    def __init__(self, username, password, created_at):
        super().__init__(username, password, created_at)

    def view_inventory(self):
        Product.view_inventory(self)

    def add_product(self, name, quantity, price):
        product = Product(name, quantity, price)
        return product

    def update_product(self, product_id, **kwargs):
        Product.product_update(self, product_id, **kwargs)
    
    def delete_product(self, product_id):
        Product.product_delete(self, product_id)