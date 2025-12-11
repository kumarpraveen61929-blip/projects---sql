import mysql.connector
from datetime import datetime

# ------------------------------
# CONNECT TO MYSQL
# ------------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",        # change if needed
    password="",        # your MySQL password
)
cursor = conn.cursor()

# ------------------------------
# 1. CREATE DATABASE
# ------------------------------
cursor.execute("CREATE DATABASE IF NOT EXISTS online_order_db")
cursor.execute("USE online_order_db")

# ------------------------------
# 2. MENU TABLE
# ------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS menu (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL
)
""")

# ------------------------------
# 3. ORDERS TABLE
# ------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    total_amount DECIMAL(10,2),
    order_date DATETIME,
    payment_status VARCHAR(20) DEFAULT 'Pending'
)
""")

# ------------------------------
# 4. ORDER ITEMS TABLE
# ------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    item_id INT,
    quantity INT,
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(item_id) REFERENCES menu(item_id)
)
""")

conn.commit()

# ------------------------------
# 5. INSERT SAMPLE MENU ITEMS
# ------------------------------
cursor.execute("SELECT COUNT(*) FROM menu")
if cursor.fetchone()[0] == 0:     # only insert once
    cursor.execute("INSERT INTO menu(item_name, price) VALUES('Burger', 120)")
    cursor.execute("INSERT INTO menu(item_name, price) VALUES('Pizza', 250)")
    cursor.execute("INSERT INTO menu(item_name, price) VALUES('Sandwich', 90)")
    cursor.execute("INSERT INTO menu(item_name, price) VALUES('Coffee', 60)")
    conn.commit()
    print("Sample menu items inserted!")

# ------------------------------
# 6. PLACE ORDER (example)
# ------------------------------
customer_name = "Praveen"
total_amount = 370
order_date = datetime.now()

cursor.execute("""
INSERT INTO orders(customer_name, total_amount, order_date)
VALUES (%s, %s, %s)
""", (customer_name, total_amount, order_date))

conn.commit()

order_id = cursor.lastrowid
print("Order placed! Order ID =", order_id)

# Add items for the order
order_items_data = [
    (order_id, 1, 2),   # 2 Burgers
    (order_id, 4, 1)    # 1 Coffee
]

cursor.executemany("""
INSERT INTO order_items(order_id, item_id, quantity)
VALUES (%s, %s, %s)
""", order_items_data)

conn.commit()
print("Order items added!")

# ------------------------------
# 7. UPDATE PAYMENT STATUS
# ------------------------------
cursor.execute("UPDATE orders SET payment_status='Paid' WHERE order_id=%s", (order_id,))
conn.commit()
print("Payment status updated to PAID.")

# ------------------------------
# 8. ORDER HISTORY
# ------------------------------
cursor.execute("""
SELECT 
    orders.order_id,
    orders.customer_name,
    menu.item_name,
    order_items.quantity,
    orders.total_amount,
    orders.payment_status,
    orders.order_date
FROM orders
JOIN order_items ON orders.order_id = order_items.order_id
JOIN menu ON order_items.item_id = menu.item_id
WHERE orders.order_id = %s
""", (order_id,))

rows = cursor.fetchall()

print("\n=== ORDER HISTORY ===")
for row in rows:
    print(row)

# ------------------------------
# CLOSE CONNECTION
# ------------------------------
cursor.close()
conn.close()
