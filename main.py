import getpass
from user import *
from product import *

init_text = "Inventory and Billing Management System"

print("_" * len(init_text))
print(init_text)
print("_" * len(init_text))

user = None
cart = None

def login():
    print("\n(Login your Account)")
    username = input("Enter your full name: ")
    password = getpass.getpass("Enter your password: ")

    logged_in_user = Cashier.login(username, password)

    # Recrsion to stop user to access without login
    if logged_in_user:
        print("(Login Successfull)")
        return logged_in_user
    print("~"*5 + " Login failed. Try again " + "~"*5)
    return login()

def cashier_feature(cart):
    print("\n(Cashier Feature)")
    print("_" * len("(Cashier Feature)"))

    print("(1) Add items to cart")
    print("(2) View product listing")
    if cart:
        print("(3) View Cart")
        print("(4) Checkout")
    print("(exit) Logout")

    # Take user input
    choice = input("Enter number or text for service: ").strip()

    try:
        if choice == "1":
            p_id = input("Enter Product ID: ").strip()
            quantity = float(input("Enter Quantity: "))
            if p_id and quantity > 0:
                if not cart:
                    cart = Cart()
                cart.add_to_cart(p_id, quantity)
            else:
                print("~" * 5 + " Invalid input " + "~" * 5)

        elif choice == "2":
            Product.view_products()

        elif choice == "3" and cart:
            cart.view_cart()

        elif choice == "4" and cart:
            cart.checkout()
            cart = None

        elif choice.lower() == "exit":
            return cart, True

        else:
            print("Invalid option.")

    except Exception as e:
        print("~" * 5 + f" Error: {e} " + "~" * 5)

    return cart, False

def admin_feature(user):
    print("\n(Admin Feature)")
    print("_" * len("(Admin Feature)"))

    print("(1) Add Product")
    print("(2) Update Product")
    print("(3) Delete Product")
    print("(4) View Inventory")
    print("(5) View Reports")
    print("(6) View product listing")
    print("(exit) Logout")

    # Take user input
    choice = input("Enter number or text for service: ").strip()

    try:
        if choice == "1":
            name = input("Enter Product Name: ").strip()
            quantity = float(input("Enter available stock: "))
            price = float(input("Enter price per unit: "))
            if name and quantity > 0 and price > 0:
                user.add_product(name, quantity, price)
            else:
                print("~" * 5 + " Invalid product input " + "~" * 5)

        elif choice == "2":
            p_id = input("Enter product ID to update: ").strip()
            p_name = input("New product name (leave blank to keep current): ").strip()
            quantity_input = input("New quantity (leave blank to keep current): ").strip()
            price_input = input("New price (leave blank to keep current): ").strip()

            quantity_input = float(quantity_input) if quantity_input else ""
            price_input = float(price_input) if price_input else ""

            user.update_product(p_id, n=p_name, s=quantity_input, p=price_input)

        elif choice == "3":
            p_id = input("Enter product ID to delete: ").strip()
            if p_id:
                user.delete_product(p_id)

        elif choice == "4":
            user.view_inventory()

        elif choice == "5":
            print("\n(1) Sales report\n(2) Inventory report")
            report_choice = input("Enter number for report: ").strip()
            user.view_report(report_choice)

        elif choice == "6":
            Product.view_products()

        elif choice.lower() == "exit":
            return True

        else:
            print("Invalid option.")

    except Exception as e:
        print("~" * 15 + f" Error: {e} " + "~" * 15)

    return False

while True:
    if not user:
        user = login()

    if user.role.lower() == "admin":
        logout = admin_feature(user)
    else:
        cart, logout = cashier_feature(cart)

    if logout:
        print("\nLogged out successfully.")
        user = None