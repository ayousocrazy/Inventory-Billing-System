import os
import time
import datetime
os.chdir(r"C:\Users\HP\Desktop\Project\Inventory and Billing Management System")

class Product:
    def __init__(self, name, quantity, price):
        name = name.replace(" ", "-") # Replacing blank spaces with (-)
        self.name = name
        self.quantity = quantity
        self.price = price

        # Create product.txt if it doesn't exist
        if not os.path.exists("billing/products.txt"):
            open("billing/products.txt", 'w').close()

        with open("billing/products.txt", 'r') as f:
            num = len(f.readlines()) + 1

        t = time.strftime("%Y%m")[2:]
        # Generate a unique Product ID
        p_id = f"{t}-{num}-{self.name[0].upper()}"

        self.__product_id = p_id

        self.save_product()

    # Save the Product object attribute to a text file
    def save_product(self):
        with open('billing/products.txt', 'a') as f:
            product_list = f"{self.__product_id} {self.name} {self.quantity} {self.price}\n"
            f.write(product_list)

    # Display Inventory method
    @staticmethod
    def view_inventory(obj):
        if type(obj).__name__.lower() == 'admin':
            doc = open('billing/products.txt', 'r')
            lines = doc.readlines()
            doc.close()
            
            print("| Product Id | Product Name | Quantity | Price |\n")

            for line in lines:
                l = line.split()
                print(f"| {l[0]} | {l[1]} | {l[2]} | {l[3]} |")

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
        doc = open('billing/products.txt', 'r')
        lines = doc.readlines()
        doc.close()

        # Take the line index (for updating) and line data
        for i, line in enumerate(lines):
            l_list = line.split()
            if product_id in l_list[0]:
                # Check what attributes to update and replace on original file line
                name = kwargs['n'].replace(" ", "-") if 'n' in kwargs else l_list[1]
                quantity = kwargs['q'] if 'q' in kwargs else l_list[2]
                price = kwargs['p'] if 'p' in kwargs else l_list[3]

                lines[i] = f"{product_id} {name} {quantity} {price}\n"

                print(f"\nProduct: {product_id} updated successfully")

                break
        else:
            print(f"\nProduct {product_id} not found")

        with open('billing/products.txt', 'w') as doc:
            doc.writelines(lines)

    # protected delete method
    @staticmethod
    def __delete_product(product_id):
        doc = open('billing/products.txt', 'r')
        lines = doc.readlines()
        doc.close()

        # Take the line index (for deleting) and line data
        for i, line in enumerate(lines):
            l_list = line.split()
            if product_id in l_list[0]:

                # Store the deleted item and datetime on deleted.txt
                with open('billing/deleted.txt', 'a') as doc:
                    content = f"Product:{l_list[0]} {l_list[1]} deleted {datetime.datetime.now()}\n"
                    doc.write(content)

                lines[i] = ""

                print(f"\nProduct: {product_id} deleted successfully")

                break
        else:
            print(f"\nProduct {product_id} not found")

        with open('billing/products.txt', 'w') as doc:
            doc.writelines(lines)