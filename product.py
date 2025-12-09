import json
import os
import time
import datetime
os.chdir(r"C:\Users\HP\Desktop\Project\Inventory and Billing Management System")

class Product:
    def __init__(self, name, stock, price):
        self.name = name
        self.stock = stock
        self.price = price

        path = "billing/products.json"

        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError: # If file is empty or corrupted
                data = []
        else:
            data = []

        num = len(data) + 1

        t = time.strftime("%Y%m")[2:]
        # Generate a unique Product ID
        p_id = f"{t}-{num}-{self.name[0].upper()}"

        self.__product_id = p_id

        self.save_product()

    # Save the Product object attribute to a json file
    def save_product(self):
        product_record = {
            'product_id' : self.__product_id,
            'name' : self.name,
            'stock' : self.stock,
            'price' : self.price
        }

        path = "billing/products.json"

        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError: # If file is empty or corrupted
                data = []
        else:
            data = []

        data.append(product_record)

        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    # Display list of available products
    @staticmethod
    def view_products():
        path = "billing/products.json"

        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError: # If file is empty or corrupted
                data = []
        else:
            data = []

        print("| Product Name | Stock |\n")

        if data:
            for l in data:
                print(f"| {l['name']} | {l['stock']} |")
        else:
            print("Stock Empty")

        print('*'*25)

    # Display Inventory details
    @staticmethod
    def view_inventory(obj):
        if type(obj).__name__.lower() == 'admin':
            path = "billing/products.json"

            if os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        data = json.load(f)
                except json.JSONDecodeError: # If file is empty or corrupted
                    data = []
            else:
                data = []

            total = 0
            
            print("| Product Id | Product Name | Stock | Price |\n")

            if data:
                for l in data:
                    total = total + (l["stock"] * l["price"])
                    print(f"| {l['product_id']} | {l['name']} | {l['stock']} | {l['price']} |")

            print('*'*25)
            print(f"Total Inventory: {total}")
            print('*'*25)

        else:
            print("Admin can only access this feature")
            print('*'*5 + "Access Denied!" + '*'*5)

    @staticmethod
    def product_update(obj, product_id, **kwargs):
        # Check if current logged in user is admin
        if type(obj).__name__.lower() == 'admin':
            Product.__update_product(product_id, **kwargs)

        else:
            print("Admin can only access this feature")
            print('*'*5 + "Access Denied!" + '*'*5)

    @staticmethod
    def product_delete(obj, product_id):
        # Check if current logged in user is admin
        if type(obj).__name__.lower() == 'admin':
            Product.__delete_product(product_id)

        else:
            print("Admin can only access this feature")
            print('*'*5 + "Access Denied!" + '*'*5)

    # protected update method
    @staticmethod
    def __update_product(product_id, **kwargs):
        path = "billing/products.json"

        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    products = json.load(f)
            except json.JSONDecodeError:
                products = []
        else:
            products = []

        # Check what attributes to update
        for p in products:
            if p["product_id"] == product_id:

                if "n" in kwargs:
                    p["name"] = kwargs["n"]

                if "s" in kwargs:
                    p["stock"] = kwargs["s"]

                if "p" in kwargs:
                    p["price"] = kwargs["p"]

                print(f"\nProduct {product_id} updated successfully.")
                break
        else:
            print(f"\nProduct {product_id} not found.")
            return

        with open(path, "w") as f:
            json.dump(products, f, indent=4)

    # protected delete method
    @staticmethod
    def __delete_product(product_id):
        path = "billing/products.json"

        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    products = json.load(f)
            except json.JSONDecodeError:
                products = []
        else:
            products = []

        for p in products:
            if p["product_id"] == product_id:
                deleted_product = p
                products.remove(p)
                print(f"\nProduct: {product_id} deleted successfully")
                break
        else:
            print(f"\nProduct {product_id} not found")
            return

        with open("billing/products.json", "w") as f:
            json.dump(products, f, indent=4)

        # Log deleted products
        with open("billing/deleted.json", "a") as f:
            log = {
                "deleted_product": deleted_product,
                "deleted_at": str(datetime.datetime.now())
            }
            f.write(json.dumps(log) + "\n")

class Cart:
    def __init__(self):
        self.product_id = []
        self.name = []
        self.quantity = []
        self.total = 0

    def add_product(self, product_id, quantity):
        pass

    def checkout(self):
        pass