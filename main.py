import getpass
from user import *
from product import *

init_text = "Inventory and Billing Management System"

print("~" * len(init_text))
print(init_text)
print("~" * len(init_text))

user = None
cart = None
logout = False

def login():
    print("\n")
    print("(Login your Account)")
    username = input("Enter your full name: ")
    password = getpass.getpass("Enter your password: ")

    user = Cashier.login(username, password)

    # Recrsion to stop user to access without login
    if user is not None:
        print("(Login Successfull)")
    else:
        login()

    return user

def cashier_feature(cart):
    print("\n")
    print(load:="(Cahier Feature)")
    print("~"*len(load))

    print("(1) Add items to cart")
    print("(2) View product listing")
    if cart is not None:
        print("(3) View Cart")
        print("(4) Checkout")
    print("(exit) Logout")

    # Take user input
    input_text = "Enter numbers or text for corresponding service: "
    print('~' * len(input_text))
    cashier_input = input(input_text)

    if cashier_input == "1":
        try:
            p_id = input("Enter Product ID: ")
            quantity = float(input("Enter Quantity: "))
            if p_id and quantity and quantity > 0:
                # Create a cart object if cart is None
                if cart is None:
                    cart = Cart()
                cart.add_to_cart(p_id, quantity)
            else:
                print("*"*15 + "Error during adding to cart" + "*"*15)
        except:
            print("*"*15 + "Error during adding to cart" + "*"*15)

    elif cashier_input == "2":
        Product.view_products()

    elif cashier_input == "3" and cart is not None:
        cart.view_cart()

    elif cashier_input == "4" and cart is not None:
        cart.checkout()
        cart = None

    elif cashier_input in ["exit", "(exit)"]:
        return cart, True
    
    else:
        cashier_feature(cart)
    
    return cart, False

def admin_feature(user):
    print("\n")
    print(load:="(Admin Feature)")
    print("~"*len(load))

    print("(1) Add Product")
    print("(2) Update Product")
    print("(3) Delete Product")
    print("(4) View Inventory")
    print("(5) View Reports")
    print("(exit) Logout")

    # Take user input
    input_text = "Enter numbers or text for corresponding service: "
    print('~' * len(input_text))
    admin_input = input(input_text)

    if admin_input == "1":
        try:
            name = input("Enter Product Name: ")
            quantity = float(input("Enter available stock: "))
            price = float(input("Enter price of per unit product: "))

            if name and quantity and price and quantity > 0 and price > 0:
                user.add_product(name, quantity, price)
            else:
                print("*"*15 + "Error during getting product input" + "*"*15)
        except:
            print("*"*15 + "Error during getting product input" + "*"*15)

    elif admin_input == "2":
        try:
            p_id = input("Enter product id to update: ")

            p_name = input("New product name (leave blank to keep current): ")
            quantity_input = input("New quantity (leave blank to keep current): ").strip()
            price_input = input("New price (leave blank to keep current): ").strip()

            if quantity_input != "":
                quantity_input = float(quantity_input)
            if price_input == "":
                price_input = float(price_input)

            user.update_product(p_id, n = p_name, s = quantity_input, p = price_input)
        except:
            print("*"*15 + "Error during updating product" + "*"*15)

    elif admin_input == "3":
        try:
            p_id = input("Enter product id to delete the product: ")

            if p_id != "":
                user.delete_product()
        except:
            print("*"*15 + "Error during deleting product" + "*"*15)

    elif admin_input == "4":
        user.view_inventory()

    elif admin_input == "5":
        pass

    elif admin_input in ["exit", "(exit)"]:
        return True
    
    else:
        admin_feature(user)

    return False

while True:
    if user is None:
        user = login()

    if user.role.lower() == "admin":
        logout = admin_feature(user)
    else:
        cart, logout = cashier_feature(cart)

    if logout:
        user = None