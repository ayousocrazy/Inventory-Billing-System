import getpass
from user import Cashier
from product import Product, Cart

INIT_TEXT = "Inventory and Billing Management System"

print("_" * len(INIT_TEXT))
print(INIT_TEXT)
print("_" * len(INIT_TEXT))


def login():
    print("\n(Login your Account)")
    while True:
        username = input("Enter your full name: ").strip()
        password = getpass.getpass("Enter your password: ")

        user = Cashier.login(username, password)
        if user:
            print("(Login Successful)")
            return user

        print("~~~~~ Login failed. Try again ~~~~~")


def cashier_feature(cart):
    print("\n(Cashier Feature)")
    print("-" * 17)

    print("(1) Add items to cart")
    print("(2) View product listing")
    if cart:
        print("(3) View Cart")
        print("(4) Update Cart Item")
        print("(5) Delete Cart Item")
        print("(6) Checkout")
    print("(exit) Logout")

    choice = input("Enter option: ").strip().lower()

    try:
        if choice == "1":
            p_id = input("Enter Product ID: ").strip()
            qty = int(input("Enter Quantity: "))

            if not cart:
                cart = Cart()

            cart.add_to_cart(p_id, qty)

        elif choice == "2":
            Product.view_products()

        elif choice == "3" and cart:
            cart.view_cart()

        elif choice == "4" and cart:
            cart.view_cart()
            index = int(input("Enter item number to update: ")) - 1
            qty = int(input("Enter new quantity: "))
            cart.update_item(index, qty)

        elif choice == "5" and cart:
            cart.view_cart()
            index = int(input("Enter item number to delete: ")) - 1
            cart.delete_item(index)

        elif choice == "6" and cart:
            cart.checkout()
            cart = None

        elif choice == "exit":
            return cart, True

        else:
            print("Invalid option.")

    except ValueError:
        print("~~~~~ Invalid numeric input ~~~~~")

    return cart, False


def admin_feature(admin):
    print("\n(Admin Feature)")
    print("-" * 14)

    print("(1) Add Product")
    print("(2) Update Product")
    print("(3) Delete Product")
    print("(4) View Inventory")
    print("(5) View Reports")
    print("(6) View product listing")
    print("(exit) Logout")

    choice = input("Enter option: ").strip().lower()

    try:
        if choice == "1":
            name = input("Product name: ").strip()
            qty = int(input("Stock quantity: "))
            price = float(input("Price per unit: "))

            admin.add_product(name, qty, price)

        elif choice == "2":
            pid = input("Product ID: ").strip()
            name = input("New name (blank to keep): ").strip()
            qty = input("New quantity (blank to keep): ").strip()
            price = input("New price (blank to keep): ").strip()

            admin.update_product(
                pid,
                n=name or "",
                s=int(qty) if qty else "",
                p=float(price) if price else ""
            )

        elif choice == "3":
            pid = input("Product ID to delete: ").strip()
            admin.delete_product(pid)

        elif choice == "4":
            admin.view_inventory()

        elif choice == "5":
            print("\n(1) Sales Report\n(2) Inventory Report")
            admin.view_report(input("Choose: ").strip())

        elif choice == "6":
            Product.view_products()

        elif choice == "exit":
            return True

        else:
            print("Invalid option.")

    except ValueError:
        print("~~~~~ Invalid numeric input ~~~~~")

    return False


user = None
cart = None

while True:
    if not user:
        user = login()

    if user.role == "admin":
        logout = admin_feature(user)
    else:
        cart, logout = cashier_feature(cart)

    if logout:
        print("\nLogged out successfully.")
        user = None
        cart = None
