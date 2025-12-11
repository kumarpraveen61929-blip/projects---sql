import sqlite3
from datetime import datetime

# =======================================
# CONNECT TO DATABASE
# =======================================
conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

# =======================================
# CREATE TABLES (RUNS AUTOMATICALLY)
# =======================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    acc_no INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    balance REAL DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    acc_no INTEGER,
    type TEXT,
    amount REAL,
    date TEXT,
    FOREIGN KEY(acc_no) REFERENCES accounts(acc_no)
)
""")

conn.commit()

# =======================================
# CREATE ACCOUNT
# =======================================
def create_account():
    name = input("Enter account holder name: ")
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, 0))
    conn.commit()
    print(f"Account created successfully! Your Account Number is: {cursor.lastrowid}")

# =======================================
# DEPOSIT MONEY
# =======================================
def deposit():
    acc = int(input("Enter account number: "))
    amount = float(input("Enter deposit amount: "))

    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE acc_no = ?", (amount, acc))

    cursor.execute("INSERT INTO transactions(acc_no, type, amount, date) VALUES (?, ?, ?, ?)",
                   (acc, "Deposit", amount, datetime.now()))
    conn.commit()
    print("Deposit successful!")

# =======================================
# WITHDRAW MONEY
# =======================================
def withdraw():
    acc = int(input("Enter account number: "))
    amount = float(input("Enter withdrawal amount: "))

    cursor.execute("SELECT balance FROM accounts WHERE acc_no = ?", (acc,))
    record = cursor.fetchone()

    if record and record[0] >= amount:
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE acc_no = ?", (amount, acc))
        cursor.execute("INSERT INTO transactions(acc_no, type, amount, date) VALUES (?, ?, ?, ?)",
                       (acc, "Withdraw", amount, datetime.now()))
        conn.commit()
        print("Withdrawal successful!")
    else:
        print("Insufficient balance!")

# =======================================
# VIEW BALANCE
# =======================================
def view_balance():
    acc = int(input("Enter account number: "))
    cursor.execute("SELECT name, balance FROM accounts WHERE acc_no = ?", (acc,))
    data = cursor.fetchone()

    if data:
        print("\n--- ACCOUNT DETAILS ---")
        print("Name:", data[0])
        print("Balance:", data[1])
    else:
        print("Account not found!")

# =======================================
# TRANSACTION HISTORY
# =======================================
def transaction_history():
    acc = int(input("Enter account number: "))
    cursor.execute("SELECT type, amount, date FROM transactions WHERE acc_no = ?", (acc,))
    records = cursor.fetchall()

    if records:
        print("\n--- TRANSACTION HISTORY ---")
        for row in records:
            print(f"{row[0]} | Rs.{row[1]} | {row[2]}")
    else:
        print("No transactions yet.")

# =======================================
# MAIN MENU
# =======================================
while True:
    print("\n===== BANKING SYSTEM =====")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. View Balance")
    print("5. Transaction History")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        create_account()
    elif choice == "2":
        deposit()
    elif choice == "3":
        withdraw()
    elif choice == "4":
        view_balance()
    elif choice == "5":
        transaction_history()
    elif choice == "6":
        print("Thank you! Exiting system...")
        break
    else:
        print("Invalid option! Try again.")
