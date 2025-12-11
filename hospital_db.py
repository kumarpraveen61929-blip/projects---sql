import mysql.connector
from datetime import datetime

# ------------------------------
# CONNECT TO MYSQL
# ------------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",        # change if needed
    password=""         # enter your MySQL password
)
cursor = conn.cursor()

# ------------------------------
# 1. CREATE DATABASE
# ------------------------------
cursor.execute("CREATE DATABASE IF NOT EXISTS hospital_db")
cursor.execute("USE hospital_db")

# ------------------------------
# 2. PATIENT TABLE
# ------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    disease VARCHAR(200),
    admission_date DATETIME,
    discharge_date DATETIME
)
""")

conn.commit()

# ------------------------------
# 3. ADD SAMPLE PATIENTS (Mukesh, Prasanna, Ram Babu)
# ------------------------------
cursor.execute("SELECT COUNT(*) FROM patients")
count = cursor.fetchone()[0]

if count == 0:   # insert only once
    sample_patients = [
        ("Mukesh", 40, "Fever", datetime.now()),
        ("Prasanna", 28, "Cold & Cough", datetime.now()),
        ("Ram Babu", 55, "Blood Pressure", datetime.now())
    ]

    cursor.executemany("""
        INSERT INTO patients(name, age, disease, admission_date)
        VALUES (%s, %s, %s, %s)
    """, sample_patients)

    conn.commit()
    print("Sample patients inserted (Mukesh, Prasanna, Ram Babu)!")

# ------------------------------
# 4. UPDATE PATIENT DETAILS (example: Mukesh)
# ------------------------------
cursor.execute("""
UPDATE patients
SET disease = 'Viral Infection'
WHERE name = 'Mukesh'
""")
conn.commit()
print("Mukesh disease updated!")

# ------------------------------
# 5. DELETE PATIENT RECORD (example: delete Prasanna)
# ------------------------------
cursor.execute("DELETE FROM patients WHERE name = 'Prasanna'")
conn.commit()
print("Prasanna deleted!")

# ------------------------------
# 6. SEARCH PATIENT
# ------------------------------

# BY ID
cursor.execute("SELECT * FROM patients WHERE patient_id = 1")
result_by_id = cursor.fetchall()
print("\nSearch by ID (1):")
for row in result_by_id:
    print(row)

# BY NAME
cursor.execute("SELECT * FROM patients WHERE name LIKE '%Ram%'")
result_by_name = cursor.fetchall()
print("\nSearch by name (Ram):")
for row in result_by_name:
    print(row)

# ------------------------------
# 7. VIEW ALL PATIENTS
# ------------------------------
cursor.execute("SELECT * FROM patients ORDER BY patient_id")
all_patients = cursor.fetchall()

print("\nALL PATIENTS:")
for p in all_patients:
    print(p)

# ------------------------------
# 8. UPDATE DISCHARGE DATE (example: Mukesh)
# ------------------------------
cursor.execute("""
UPDATE patients
SET discharge_date = NOW()
WHERE name = 'Mukesh'
""")
conn.commit()
print("\nDischarge date updated for Mukesh!")

# ------------------------------
# CLOSE CONNECTION
# ------------------------------
cursor.close()
conn.close()
