import mysql.connector
from mysql.connector import Error

# --- 1. CONFIGURATION AND UTILITIES ---

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': ''
}

STUDENT_DB_NAME = 'student_db'


def connect_db():
    try:
        config = DB_CONFIG.copy()
        config['database'] = STUDENT_DB_NAME
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"❌ Database Connection Error: {e}")
    return None


def setup_student_table():
    try:
        conn_base = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn_base.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {STUDENT_DB_NAME}")
        conn_base.close()
    except Error as e:
        print(f"❌ Error setting up database: {e}")
        return

    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Students (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                class VARCHAR(50),
                marks DECIMAL(5,2)
            )
        ''')
        conn.commit()
    except Error as e:
        print(f"❌ Error creating table: {e}")
    finally:
        cursor.close()
        conn.close()


setup_student_table()

# --- 2. FUNCTIONS ---


def add_new_student(name, age, class_name, marks):
    conn = connect_db()
    if conn is None: return
    cursor = conn.cursor()
    query = 'INSERT INTO Students (name, age, class, marks) VALUES (%s, %s, %s, %s)'
    try:
        cursor.execute(query, (name, age, class_name, marks))
        conn.commit()
        print(f"✅ Student '{name}' added successfully.")
    except Error as e:
        print(f"❌ Error adding student: {e}")
    finally:
        cursor.close()
        conn.close()


def update_student_info(student_id, age=None, class_name=None, marks=None):
    conn = connect_db()
    if conn is None: return
    cursor = conn.cursor()

    updates = []
    params = []

    if age is not None:
        updates.append("age = %s")
        params.append(age)
    if class_name is not None:
        updates.append("class = %s")
        params.append(class_name)
    if marks is not None:
        updates.append("marks = %s")
        params.append(marks)

    if not updates:
        print("⚠️ Nothing to update!")
        return

    params.append(student_id)

    query = f"UPDATE Students SET {', '.join(updates)} WHERE ID = %s"

    cursor.execute(query, params)
    conn.commit()

    if cursor.rowcount > 0:
        print(f"🔄 Student ID {student_id} updated successfully.")
    else:
        print(f"❌ No student found with ID {student_id}")

    cursor.close()
    conn.close()


def delete_student(student_id):
    conn = connect_db()
    if conn is None: return
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Students WHERE ID = %s', (student_id,))
    conn.commit()

    if cursor.rowcount > 0:
        print("🗑️ Student deleted successfully.")
    else:
        print("❌ Student ID not found.")

    cursor.close()
    conn.close()


def view_all_students():
    conn = connect_db()
    if conn is None: return
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Students ORDER BY ID")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    print("\n--- 📚 STUDENT LIST ---")
    if rows:
        for s in rows:
            print(f"ID: {s['ID']} | Name: {s['name']} | Age: {s['age']} | Class: {s['class']} | Marks: {s['marks']}")
    else:
        print("⚠️ No students found!")
    print("------------------------------\n")


def search_student(query):
    conn = connect_db()
    if conn is None: return
    cursor = conn.cursor(dictionary=True)

    try:
        num = int(query)
        cursor.execute("SELECT * FROM Students WHERE ID = %s", (num,))
    except ValueError:
        cursor.execute("SELECT * FROM Students WHERE name LIKE %s", (f"%{query}%",))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    print(f"\n--- 🔍 Search Results for '{query}' ---")
    if results:
        for s in results:
            print(f"ID: {s['ID']} | Name: {s['name']} | Age: {s['age']} | Class: {s['class']} | Marks: {s['marks']}")
    else:
        print("❌ No matching students found.")
    print("-----------------------------------\n")


# --- 3. MENU SYSTEM ---

def menu():
    while True:
        print("\n====== STUDENT MANAGEMENT SYSTEM ======")
        print("1. Add new student")
        print("2. Update student info")
        print("3. Delete student")
        print("4. View all students")
        print("5. Search by name or ID")
        print("6. Exit")
        print("=======================================")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            class_name = input("Enter class: ")
            marks = float(input("Enter marks: "))
            add_new_student(name, age, class_name, marks)

        elif choice == "2":
            sid = int(input("Enter Student ID: "))
            print("Leave blank if no change.")
            age = input("New age: ")
            class_name = input("New class: ")
            marks = input("New marks: ")

            update_student_info(
                sid,
                age=int(age) if age else None,
                class_name=class_name if class_name else None,
                marks=float(marks) if marks else None
            )

        elif choice == "3":
            sid = int(input("Enter Student ID to delete: "))
            delete_student(sid)

        elif choice == "4":
            view_all_students()

        elif choice == "5":
            q = input("Enter name or ID to search: ")
            search_student(q)

        elif choice == "6":
            print("👋 Exiting program...")
            break

        else:
            print("❌ Invalid choice! Enter 1–6 only.")


if __name__ == "__main__":
    menu()
