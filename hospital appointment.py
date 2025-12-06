
import sqlite3

DB_NAME = "hospital.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            phone TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(id)
        )
    """)

    conn.commit()
    conn.close()

def add_doctor():
    print("\n--- Add Doctor ---")
    name = input("Doctor name        : ").strip()
    specialization = input("Specialization     : ").strip()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO doctors (name, specialization) VALUES (?, ?)",
                (name, specialization))
    conn.commit()
    conn.close()
    print("✔ Doctor added!")

def list_doctors():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, specialization FROM doctors")
    rows = cur.fetchall()
    conn.close()

    print("\n--- Doctors ---")
    if not rows:
        print("No doctors found.")
        return

    for row in rows:
        print(f"[{row[0]}] {row[1]} ({row[2]})")

def add_patient():
    print("\n--- Add Patient ---")
    name = input("Patient name   : ").strip()
    try:
        age = int(input("Age            : ").strip())
    except ValueError:
        age = None
    gender = input("Gender (M/F/O) : ").strip()
    phone = input("Phone          : ").strip()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO patients (name, age, gender, phone)
        VALUES (?, ?, ?, ?)
    """, (name, age, gender, phone))
    conn.commit()
    conn.close()
    print("✔ Patient added!")

def list_patients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, age, gender, phone FROM patients")
    rows = cur.fetchall()
    conn.close()

    print("\n--- Patients ---")
    if not rows:
        print("No patients found.")
        return

    for row in rows:
        id_, name, age, gender, phone = row
        print(f"[{id_}] {name}, Age: {age}, Gender: {gender}, Phone: {phone}")

def book_appointment():
    print("\n--- Book Appointment ---")
    list_patients()
    try:
        patient_id = int(input("Enter Patient ID: ").strip())
    except ValueError:
        print("❌ Invalid Patient ID.")
        return

    list_doctors()
    try:
        doctor_id = int(input("Enter Doctor ID : ").strip())
    except ValueError:
        print("❌ Invalid Doctor ID.")
        return

    date = input("Date (YYYY-MM-DD): ").strip()
    time = input("Time (HH:MM)     : ").strip()
    status = "Scheduled"

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO appointments (patient_id, doctor_id, date, time, status)
        VALUES (?, ?, ?, ?, ?)
    """, (patient_id, doctor_id, date, time, status))
    conn.commit()
    conn.close()
    print("✔ Appointment booked!")

def list_appointments():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id, p.name, d.name, d.specialization, a.date, a.time, a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        ORDER BY a.date, a.time
    """)
    rows = cur.fetchall()
    conn.close()

    print("\n--- Appointments ---")
    if not rows:
        print("No appointments found.")
        return

    for row in rows:
        app_id, p_name, d_name, spec, date, time, status = row
        print(f"[{app_id}] {date} {time} | {p_name} -> Dr. {d_name} ({spec}) | {status}")

def main():
    create_tables()
    while True:
        print("\n=== Hospital Management ===")
        print("1. Add doctor")
        print("2. Add patient")
        print("3. Book appointment")
        print("4. List doctors")
        print("5. List patients")
        print("6. List appointments")
        print("7. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_doctor()
        elif choice == "2":
            add_patient()
        elif choice == "3":
            book_appointment()
        elif choice == "4":
            list_doctors()
        elif choice == "5":
            list_patients()
        elif choice == "6":
            list_appointments()
        elif choice == "7":
            print("Bye!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
