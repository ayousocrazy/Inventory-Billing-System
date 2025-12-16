import getpass
from user import *

INIT_TEXT = "Admin Panel"


def print_header(text):
    print("\n" + "~" * len(text))
    print(text)
    print("~" * len(text))


def admin_login():
    print("\n(Login your Account)")
    while True:
        username = input("Enter your full name: ").strip()
        password = getpass.getpass("Enter your password: ")

        logged_user = Cashier.login(username, password)

        if logged_user and logged_user.role.lower() == "admin":
            print("(Admin Login Successful)")
            return logged_user
        else:
            print("(Admin access denied – try again)\n")


def get_choice():
    print("\nOptions")
    print("-" * 7)
    print("(1) Add new user account")
    print("(2) View users")
    print("(3) Update user")
    print("(4) Delete user")
    print("(exit) Logout")
    return input("Enter option: ").strip().lower()


print_header(INIT_TEXT)

admin = None

while True:
    if admin is None:
        admin = admin_login()

    choice = get_choice()

    # ---------------- ADD USER ----------------
    if choice == "1":
        name = input("Enter username: ").strip()
        password = input("Enter a temporary password: ").strip()
        role = input("(a) admin\n(c) cashier\nEnter account role: ").strip().lower()

        role_map = {"a": "admin", "c": "cashier"}

        if role in role_map:
            admin.save_user(name, password, role_map[role])
            print(f"({name} added as {role_map[role]})")
        else:
            print("~~~~~ Error ~~~~~")
            print("Role not clear")

    # ---------------- VIEW USERS ----------------
    elif choice == "2":
        admin.view_users()

    # ---------------- UPDATE USER ----------------
    elif choice == "3":
        users = admin.view_users()

        try:
            index = int(input("Enter user number to update: ")) - 1
            if index < 0 or index >= len(users):
                raise ValueError

            new_name = input("New username (leave blank to keep): ").strip()
            new_password = input("New password (leave blank to keep): ").strip()
            role_input = input("(a) admin (c) cashier (leave blank to keep): ").strip().lower()

            role_map = {"a": "admin", "c": "cashier"}
            new_role = role_map.get(role_input, "")

            admin.update_user(index, new_name, new_password, new_role)

        except ValueError:
            print("Invalid user number")

    # ---------------- DELETE USER ----------------
    elif choice == "4":
        users = admin.view_users()

        try:
            index = int(input("Enter user number to delete: ")) - 1
            if index < 0 or index >= len(users):
                raise ValueError

            admin.delete_user(index)

        except ValueError:
            print("Invalid user number")

    # ---------------- LOGOUT ----------------
    elif choice == "exit":
        print("(Account logout)")
        admin = None

    # ---------------- INVALID OPTION ----------------
    else:
        print("~~~~~ Option not available ~~~~~")
