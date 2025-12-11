import mysql.connector
from mysql.connector import Error

# -------------------------------------------------
# INVENTORY MANAGEMENT SYSTEM (Single Program File)
# -------------------------------------------------

# MySQL Configuration (XAMPP Default)
HOST = "localhost"
USER = "root"
PASSWORD = ""
DB_NAME = "inventory_db"

# -------------------------------------------------
# CREATE DATABASE + TABLE (Runs inside program)
# -------------------------------------------------

def create_database_and_table():
    try:
        # Connect without database to create one
        conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.close()
    except Error as e:
        print("❌ Database Creation Error:", e)

    # Connect again WITH the database
    try:
        conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                price DECIMAL(10,2),
                quantity INT
            )
        """)
        conn.commit()

        cursor.close()
        conn.close()

    except Error as e:
        print("❌ Table Creation Error:", e)


# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------

def connect_db():
    try:
        conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        return conn
    except Error as e:
        print("❌ Connection Error:", e)
        return None


# -------------------------------------------------
# INVENTORY FUNCTIONS
# -------------------------------------------------

def add_product(name, price, quantity):
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO Products (name, price, quantity) VALUES (%s, %s, %s)",
            (name, price, quantity)
        )
        conn.commit()
        print(f"✅ Product '{name}' added successfully.")
    except Error as e:
        print("❌ Error adding product:", e)

    cursor.close()
    conn.close()


def update_product(pid, new_price=None, new_qty=None):
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()

    query_parts = []
    values = []

    if new_price is not None:
        query_parts.append("price = %s")
        values.append(new_price)

    if new_qty is not None:
        query_parts.append("quantity = %s")
        values.append(new_qty)

    if not query_parts:
        print("⚠️ No update values provided.")
        return

    values.append(pid)

    query = f"UPDATE Products SET {', '.join(query_parts)} WHERE ID = %s"

    try:
        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount > 0:
            print(f"🔄 Product ID {pid} updated successfully.")
        else:
            print("❌ Product not found.")
    except Error as e:
        print("❌ Error updating product:", e)

    cursor.close()
    conn.close()


def delete_product(pid):
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Products WHERE ID = %s", (pid,))
    conn.commit()

    if cursor.rowcount > 0:
        print("🗑️ Product deleted successfully.")
    else:
        print("❌ Product ID not found.")

    cursor.close()
    conn.close()


def check_stock():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Products ORDER BY ID")
    rows = cursor.fetchall()

    print("\n------ 🏪 CURRENT STOCK ------")
    if rows:
        for p in rows:
            print(f"ID: {p['ID']} | Name: {p['name']} | Price: {p['price']} | Qty: {p['quantity']}")
    else:
        print("⚠️ No products in inventory.")
    print("------------------------------\n")

    cursor.close()
    conn.close()


def generate_report():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()

    # Total quantity
    cursor.execute("SELECT SUM(quantity) FROM Products")
    total_qty = cursor.fetchone()[0] or 0

    # Total stock value
    cursor.execute("SELECT SUM(price * quantity) FROM Products")
    total_value = cursor.fetchone()[0] or 0.0

    print("\n------ 📊 INVENTORY REPORT ------")
    print(f"Total units in stock      : {total_qty}")
    print(f"Total inventory value (₹) : {total_value:.2f}")
    print("---------------------------------\n")

    cursor.close()
    conn.close()


# -------------------------------------------------
# MENU SYSTEM
# -------------------------------------------------

def menu():
    # Ensure DB + table created
    create_database_and_table()

    while True:
        print("\n======== INVENTORY MANAGEMENT ========")
        print("1. Add product")
        print("2. Update product info")
        print("3. Delete product")
        print("4. Check stock")
        print("5. Generate report")
        print("6. Exit")
        print("======================================")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            name = input("Product name: ")
            price = float(input("Price: "))
            qty = int(input("Quantity: "))
            add_product(name, price, qty)

        elif choice == "2":
            pid = int(input("Product ID: "))
            print("Leave blank if no change.")
            price = input("New price: ")
            qty = input("New quantity: ")

            update_product(
                pid,
                new_price=float(price) if price else None,
                new_qty=int(qty) if qty else None
            )

        elif choice == "3":
            pid = int(input("Product ID to delete: "))
            delete_product(pid)

        elif choice == "4":
            check_stock()

        elif choice == "5":
            generate_report()

        elif choice == "6":
            print("👋 Exiting program...")
            break

        else:
            print("❌ Invalid option! Please choose 1–6.")


# -------------------------------------------------
# RUN PROGRAM
# -------------------------------------------------

if __name__ == "__main__":
    menu()
