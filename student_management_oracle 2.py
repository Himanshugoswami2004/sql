#!/usr/bin/env python3
"""
Student Management System (Python + SQLite fallback for cx_Oracle)
"""

import sqlite3

DB_FILE = "students.db"

# ──────────────────────────────────────────────────────────────────────────────
# Database Connection Setup (SQLite fallback)
# ──────────────────────────────────────────────────────────────────────────────

def connect_db():
    return sqlite3.connect(DB_FILE)

def init_db():
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                roll_no INTEGER PRIMARY KEY,
                name TEXT,
                course TEXT,
                marks REAL
            )
        """)
        conn.commit()
        print("[✓] Table 'students' is ready.")

# ──────────────────────────────────────────────────────────────────────────────
# Functionalities
# ──────────────────────────────────────────────────────────────────────────────

def add_student_auto(roll, name, course, marks):
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO students (roll_no, name, course, marks)
            VALUES (?, ?, ?, ?)
        """, (roll, name, course, marks))
        conn.commit()
        print(f"[+] Student added: {roll}, {name}, {course}, {marks}")

def view_students():
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students ORDER BY roll_no")
        rows = cur.fetchall()
        if not rows:
            print("No students found.")
            return
        print("\n{:<10} {:<20} {:<15} {:<5}".format("Roll No", "Name", "Course", "Marks"))
        print("-" * 55)
        for row in rows:
            print("{:<10} {:<20} {:<15} {:<5}".format(*row))
        print("-" * 55)

def delete_student_auto(roll):
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE roll_no = ?", (roll,))
        conn.commit()
        print(f"[✘] Student with roll {roll} deleted.")

def update_marks_auto(roll, new_marks):
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE students SET marks = ? WHERE roll_no = ?", (new_marks, roll))
        conn.commit()
        print(f"[~] Marks updated for roll {roll} to {new_marks}.")

# ──────────────────────────────────────────────────────────────────────────────
# Main Flow for Testing in Non-Interactive Mode
# ──────────────────────────────────────────────────────────────────────────────

def main():
    init_db()

    # Sample test data with 10 students
    test_students = [
        (101, "Amit Kumar", "BCA", 88.5),
        (102, "Lucky Bhardwaj", "BCA", 75.0),
        (103, "Sneha Sharma", "BBA", 91.0),
        (104, "Ravi Verma", "MCA", 65.0),
        (105, "Simran Kaur", "BCA", 82.0),
        (106, "Mohit Rana", "BBA", 79.5),
        (107, "Anjali Mehta", "BCA", 85.0),
        (108, "Raj Patel", "MCA", 68.0),
        (109, "Nikita Joshi", "BBA", 92.0),
        (110, "Karan Singh", "BCA", 73.5)
    ]

    for roll, name, course, marks in test_students:
        add_student_auto(roll, name, course, marks)

    view_students()

    # Simulate update and delete
    update_marks_auto(102, 78.5)
    delete_student_auto(103)
    view_students()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[✘] Interrupted. Exiting...")
