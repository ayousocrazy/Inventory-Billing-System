import getpass
from user import *

init_text = "Admin Panel"

user = None

print("\n" + "~" * len(init_text))
print(init_text)
print("~" * len(init_text))

def login():
    print("\n(Login your Account)")
    username = input("Enter your full name: ").strip()
    password = getpass.getpass("Enter your password: ")

    logged_user = Cashier.login(username, password)

    # Recrsion to stop user to access without login
    if logged_user and logged_user.role.lower() == "admin":
        print("(Admin Login Successful)")
        return logged_user
    else:
        print("(Admin access denied)")
        return login()

while True:
    if user is None:
        user = login()

    print("\nOptions")
    print("-" * len("Options"))

    print("(1) Add new user account")
    print("(exit) Logout")
    choice = input("Enter option for corresponding feature: ").strip().lower()

    if choice in ["1", "(1)"]:
        name = input("Enter username: ").strip()
        password = input("Enter a temporary password: ").strip()
        role = input("(a) admin\n(c) cashier\nEnter account role: ")

        if role.lower() in ["a", "(a)"]:
            user.save_user(name, password, "admin")
            print(f"({name} added)")
        elif role.lower() in ["c", "(c)"]:
            user.save_user(name, password, "cashier")
            print(f"({name} added)")
        else:
            print("~"*5 + " Error " + "~"*5)
            print("~"*5 + " Role not clear " + "~"*5)

    elif choice in ["exit", "(exit)"]:
        print("(Account logout)")
        user = None

    else:
        print("~"*5 + " Option not available " + "~"*5)