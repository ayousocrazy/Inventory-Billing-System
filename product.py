import json, os, time, datetime

os.chdir(r"C:\Users\HP\Desktop\Project\Inventory and Billing Management System")

PRODUCT_FILE = "billing/products.json"
SALES_FILE = "billing/sales.json"
DELETED_FILE = "billing/deleted.json"
BILLS_DIR = "billing/bills"

os.makedirs(BILLS_DIR, exist_ok=True)

class Product:
    def __init__(self, name, stock, price):
        self.name = name
        self.stock = stock
        self.price = price

        data = self._load_product_file()

        num = len(data) + 1
        t = time.strftime("%Y%m")[2:]
        # Generate a unique Product ID
        self.__product_id = f"{t}-{num}-{self.name[0].upper()}"

        self.save_product()

    def _load_product_file(self):
        if not os.path.exists(PRODUCT_FILE):
            return []

        try:
            with open(PRODUCT_FILE, "r") as f:
                return json.load(f)
        except:
            return []

    # Save the Product object attribute to a json file
    def save_product(self):
        data = self._load_product_file()

        product_record = {
            'product_id' : self.__product_id,
            'name' : self.name,
            'stock' : self.stock,
            'price' : self.price
        }

        data.append(product_record)

        with open(PRODUCT_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    # Display list of available products
    @staticmethod
    def view_products():
        data = Product._static_load()

        if data:
            print("\n| Product Name | Stock |\n")
            for l in data:
                print(f"| {l['name']} | {l['stock']} |")
        else:
            print("Stock Empty")
        print('_'*25)

    # Display Inventory details
    @staticmethod
    def view_inventory(user):
        if type(user).__name__.lower() != "admin":
            print("Admin can only access this feature")
            print("~"*5 + "Access denied" + "~"*5)
            return

        data = Product._static_load()

        if not data:
            print("~"*5 + "Stock Empty" + "~"*5)
            return

        total = 0

        print("\n| Product Id | Product Name | Stock | Price |\n")
        for p in data:
            total = total + (p["stock"] * p["price"])
            print(f"| {p['product_id']} | {p['name']} | {p['stock']} | {p['price']} |")
                

        print('_'*25)
        print(f"Total Inventory: {total}")
        print('_'*25)

    @staticmethod
    def product_update(user, product_id, **kwargs):
        # Check if current logged in user is admin
        if type(user).__name__.lower() == 'admin':
            Product.__update_product(product_id, **kwargs)

        else:
            print("Admin can only access this feature")
            print('~'*5 + " Access Denied! " + '~'*5)

    @staticmethod
    def product_delete(user, product_id):
        # Check if current logged in user is admin
        if type(user).__name__.lower() == 'admin':
            Product.__delete_product(product_id)

        else:
            print("Admin can only access this feature")
            print('~'*5 + " Access Denied! " + '~'*5)

    # protected update method
    @staticmethod
    def __update_product(product_id, **kwargs):
        data = Product._static_load()

        # Check what attributes to update
        for p in data:
            if p["product_id"] == product_id:
                if kwargs.get("n"): p["name"] = kwargs["n"]
                if kwargs.get("s"): p["stock"] = int(kwargs["s"])
                if kwargs.get("p"): p["price"] = float(kwargs["p"])

                with open(PRODUCT_FILE, "w") as f:
                    json.dump(data, f, indent=4)

                print(f"\nProduct {product_id} updated successfully.")
                return
        
        print(f"\nProduct {product_id} not found.")

    # protected delete method
    @staticmethod
    def __delete_product(product_id):
        data = Product._static_load()

        for p in data:
            if p["product_id"] == product_id:
                data.remove(p)

                with open(PRODUCT_FILE, "w") as f:
                    json.dump(data, f, indent=4)

                # Log deleted products
                with open(DELETED_FILE, "a") as f:
                    log = {
                        "deleted_product": p,
                        "deleted_at": str(datetime.datetime.now())
                    }
                    f.write(json.dumps(log) + "\n")

                print(f"\nProduct: {product_id} deleted successfully")
                return
            
        print(f"\nProduct {product_id} not found")

    @staticmethod
    def _static_load():
        if not os.path.exists(PRODUCT_FILE):
            return []
        try:
            with open(PRODUCT_FILE, "r") as f:
                return json.load(f)
        except:
            return []

class Cart:
    def __init__(self):
        self.items = [] 
        self.total = 0

    def add_to_cart(self, product_id, quantity):
        quantity = int(quantity)
        data = Product._static_load()

        for p in data:
            if p["product_id"] == product_id:

                # Check is the 
                if p["stock"] < quantity:
                    remain = quantity - p['stock']
                    quantity = p['stock']
                    print("\n")
                    print("~"*5 + f"Only {p['stock']} available for {p['name']}" + "~"*5)
                    print("~"*5 + f"{remain} unit not available" + "~"*5)

                self.items.append({
                    "product_id": product_id,
                    "name": p["name"],
                    "qty": quantity,
                    "price": p["price"]
                })

                self.total += quantity * p["price"]

                print("Added to cart.")
                self.view_cart()
                return
            
        print(f"\nProduct {product_id} not found")

    def view_cart(self):
        if not self.items:
            print("Cart empty")
            return
        
        print("\n(Cart Details)")
        print("| S.N. | Product ID | Product | Quantity |")

        for i, item in enumerate(self.items):
            print(f"| {i+1} | {item['product_id']} | {item['name']} | {item['qty']} | {item['price']} |")

        print("Total =", self.total)
    
    def checkout(self):
        if not self.items:
            print("Cart empty")
            return

        products = Product._static_load()
        pid_map = {p["product_id"]: p for p in products}

        for item in self.items:
            pid_map[item["product_id"]]["stock"] -= item["qty"]

        with open(PRODUCT_FILE, "w") as f:
            json.dump(list(pid_map.values()), f, indent=4)

        # save bill
        bill_path = f"{BILLS_DIR}/bill-{int(time.time())}.json"
        with open(bill_path, "w") as f:
            json.dump({
                "items": self.items,
                "total": self.total,
                "created_at": str(datetime.datetime.now())
            }, f, indent=4)

        # update sales
        today = time.strftime("%Y-%m-%d")
        sales = []

        if os.path.exists(SALES_FILE):
            try:
                with open(SALES_FILE, "r") as f:
                    sales = json.load(f)
            except:
                sales = []

        for s in sales:
            if s["date"] == today:
                for item in self.items:
                    s["product_list"].append({
                        "product_id": item["product_id"],
                        "quantity": item["qty"]
                    })
                break
        else:
            sales.append({
                "date": today,
                "product_list": [
                    {"product_id": item["product_id"], "quantity": item["qty"]}
                    for item in self.items
                ]
            })

        with open(SALES_FILE, "w") as f:
            json.dump(sales, f, indent=4)

        print("\nCheckout complete!")
        print("Bill saved at:", bill_path)

        self.items.clear()
        self.total = 0