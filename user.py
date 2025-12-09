import os
import time
os.chdir(r"C:\Users\HP\Desktop\Project\Inventory and Billing Management System")

class Cashier:
    def __init__(self, username, password):
        self.username = username
        self.__password = password
        self.created_at = time.time()
        self.save_user()

    def save_user(self):
        role = "admin" if type(self).__name__.lower() == "admin" else "cashier"

        with open("billing/users.txt", 'a') as doc:
            doc_list = f"{self.username} {self.__password} {role} {self.created_at}\n"
            doc.write(doc_list)

class Admin(Cashier):
    def __init__(self, username, password, created_at):
        super().__init__(username, password, created_at)