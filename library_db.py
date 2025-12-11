import sqlite3
from datetime import datetime

# ============================================================
# CONNECT TO DATABASE
# ============================================================
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# ============================================================
# CREATE TABLES (SQL CODE INSIDE PYTHON)
# ============================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT,
    quantity INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS issued_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    issue_date TEXT,
    return_date TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(book_id) REFERENCES books(book_id)
)
""")

conn.commit()

# ============================================================
# ADD BOOK
# ============================================================
def add_book():
    title = input("Enter Book Title: ")
    author = input("Enter Author: ")
    qty = int(input("Enter Quantity: "))

    cursor.execute(
        "INSERT INTO books(title, author, quantity) VALUES (?, ?, ?)",
        (title, author, qty)
    )
    conn.commit()
    print("Book added successfully!")

# ============================================================
# UPDATE BOOK
# ============================================================
def update_book():
    book_id = int(input("Enter Book ID to update: "))
    title = input("New Title: ")
    author = input("New Author: ")
    qty = int(input("New Quantity: "))

    cursor.execute(
        "UPDATE books SET title=?, author=?, quantity=? WHERE book_id=?",
        (title, author, qty, book_id)
    )
    conn.commit()
    print("Book updated successfully!")

# ============================================================
# DELETE BOOK
# ============================================================
def delete_book():
    book_id = int(input("Enter Book ID to delete: "))
    cursor.execute("DELETE FROM books WHERE book_id=?", (book_id,))
    conn.commit()
    print("Book deleted successfully!")

# ============================================================
# REGISTER USER
# ============================================================
def register_user():
    name = input("Enter User Name: ")
    cursor.execute("INSERT INTO users(name) VALUES (?)", (name,))
    conn.commit()
    print("User registered successfully!")

# ============================================================
# ISSUE BOOK
# ============================================================
def issue_book():
    user_id = int(input("Enter User ID: "))
    book_id = int(input("Enter Book ID: "))

    cursor.execute("SELECT quantity FROM books WHERE book_id=?", (book_id,))
    book = cursor.fetchone()

    if not book:
        print("Book not found!")
        return

    if book[0] <= 0:
        print("Book is out of stock!")
        return

    cursor.execute(
        "INSERT INTO issued_books(user_id, book_id, issue_date) VALUES (?, ?, ?)",
        (user_id, book_id, datetime.now())
    )

    cursor.execute(
        "UPDATE books SET quantity = quantity - 1 WHERE book_id=?",
        (book_id,)
    )

    conn.commit()
    print("Book issued successfully!")

# ============================================================
# RETURN BOOK
# ============================================================
def return_book():
    issue_id = int(input("Enter Issue ID (From issued list): "))

    cursor.execute(
        "SELECT book_id FROM issued_books WHERE id=? AND return_date IS NULL",
        (issue_id,)
    )
    data = cursor.fetchone()

    if not data:
        print("Invalid issue ID or already returned!")
        return

    book_id = data[0]

    cursor.execute(
        "UPDATE issued_books SET return_date=? WHERE id=?",
        (datetime.now(), issue_id)
    )

    cursor.execute(
        "UPDATE books SET quantity = quantity + 1 WHERE book_id=?",
        (book_id,)
    )

    conn.commit()
    print("Book returned successfully!")

# ============================================================
# VIEW ISSUED BOOKS
# ============================================================
def view_issued_books():
    cursor.execute("""
        SELECT issued_books.id, users.name, books.title, issued_books.issue_date, issued_books.return_date
        FROM issued_books
        JOIN users ON issued_books.user_id = users.user_id
        JOIN books ON issued_books.book_id = books.book_id
    """)
    rows = cursor.fetchall()

    print("\n--- Issued Books List ---")
    for r in rows:
        print(f"Issue ID: {r[0]}, User: {r[1]}, Book: {r[2]}, Issued: {r[3]}, Returned: {r[4]}")
    print("----------------------------\n")

# ============================================================
# MAIN MENU
# ============================================================
while True:
    print("\n======== LIBRARY MANAGEMENT SYSTEM ========")
    print("1. Add Book")
    print("2. Update Book")
    print("3. Delete Book")
    print("4. Register User")
    print("5. Issue Book")
    print("6. Return Book")
    print("7. View Issued Books")
    print("8. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        update_book()
    elif choice == "3":
        delete_book()
    elif choice == "4":
        register_user()
    elif choice == "5":
        issue_book()
    elif choice == "6":
        return_book()
    elif choice == "7":
        view_issued_books()
    elif choice == "8":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Try again.")
