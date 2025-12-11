import getpass
from user import *

init_text = "Admin Panel"

user = None

print("\n")
print("~" * len(init_text))
print(init_text)
print("~" * len(init_text))

def login():
    print("\n")
    print("(Login your Account)")
    username = input("Enter your full name: ")
    password = getpass.getpass("Enter your password: ")

    user = Cashier.login(username, password)

    # Recrsion to stop user to access without login
    if user is not None:
        if user.role == "admin":
            print("(Admin Login Successfull)")
        else:
            print("(Admin access denied)")
            login()
    else:
        print("(Admin access denied)")
        login()

    return user

while True:
    if user is None:
        user = login()

    print("\n")
    print(o_text:="Options")
    print("-"*len(o_text))

    print("(1) Add new user account")
    print("(exit) Logout")
    i = input("Enter option for corresponding feature: ")

    if i in ["1", "(1)"]:
        name = input("Enter username: ")
        password = input("Enter a temporary password: ")
        role = input("(a) admin\n(c) cashier\nEnter account role: ")
        if role.lower() in ["a", "(a)"]:
            user.save_user(name, password, "admin")
            print(f"({name} added)")
        elif role.lower() in ["c", "(c)"]:
            user.save_user(name, password, "cashier")
            print(f"({name} added)")
        else:
            print("*"*15 + "Error" + "*"*15)
            print("*"*15 + "Role not clear" + "*"*15)

    elif i in ["exit", "(exit)"]:
        print("(Account logout)")
        user = None

    else:
        print("*"*15 + "Option not available" + "*"*15)