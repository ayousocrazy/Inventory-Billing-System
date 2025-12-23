# Inventory-Billing-System 🛒💳

A complete command-line-based Inventory and Billing System with **role-based access** (Admin and Cashier), JSON-based data storage, and basic encryption for sensitive data.  
This system allows admins to manage products and users, and cashiers to manage customer orders and checkout efficiently.

---

## 📂 Repository Structure

```
Inventory-Billing-System/
│
├── billing/                  # Data storage folder
│   ├── bills/                # Generated bills
│   ├── deleted.json          # Deleted products record
│   ├── sales.json            # Sales data
│   ├── products.json         # Product data
│   └── users.json            # User accounts data
│
├── admin.py                  # Admin interface and functionalities
├── main.py                   # Cashier interface / main program
├── product.py                # Product-related operations
├── user.py                   # User-related operations
└── README.md                 # This file
```

---

## 🔹 Features

### Admin
Admins have full control over the system:

- **User Management**
  - Add new user accounts
  - View existing users
  - Update user information
  - Delete users

- **Product Management**
  - Add new products
  - Update existing products
  - Delete products
  - View inventory
  - View product listings

- **Reports**
  - Sales reports
  - Inventory reports

---

### Cashier
Cashiers can manage sales and orders:

- Add items to the cart
- View product listing
- View, update, and delete cart items (if cart has items)
- Checkout and generate bills

---

### Security & Data Storage
- Password-protected system for users
- Bills and user/product data stored in **JSON files**
- Simple **XOR-based encryption** for sensitive data:

```python
@staticmethod
def xor_encrypt(text, key=42):
    return "".join(chr(ord(c) ^ key) for c in text)

@staticmethod
def xor_decrypt(text, key=42):
    return "".join(chr(ord(c) ^ key) for c in text)
```
