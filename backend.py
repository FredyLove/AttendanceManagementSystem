import sqlite3
import os
import pandas as pd

DB_NAME = "attendance.db"

def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            attendance INTEGER DEFAULT 0,
            marks INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def import_class_list(file_path):
    try:
        if file_path.endswith(".txt"):
            with open(file_path, "r") as file:
                names = [line.strip() for line in file.readlines()]
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
            names = df["Name"].tolist()

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        for name in names:
            cursor.execute("INSERT OR IGNORE INTO students (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def add_student(name):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        pass  # Student already exists

def update_marks(student_name, marks_change):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT marks FROM students WHERE name=?", (student_name,))
    current_marks = cursor.fetchone()

    if current_marks is not None:
        new_marks = current_marks[0] + marks_change  # Add or subtract marks
        cursor.execute("UPDATE students SET marks=? WHERE name=?", (new_marks, student_name))
        conn.commit()
        conn.close()

        return new_marks 
    else:
        conn.close()
        raise ValueError("Student not found!")

def get_students():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, attendance, marks FROM students")
    students = [{"name": row[0], "attendance": row[1], "marks": row[2]} for row in cursor.fetchall()]
    conn.close()
    return students

def mark_attendance(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET attendance = attendance + 1 WHERE name = ?", (name,))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, attendance FROM students")
    stats = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return stats

def clear_class_list():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students")
    conn.commit()
    conn.close()

def delete_student(student_name):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE name=?", (student_name,))
    conn.commit()
    conn.close()


initialize_db()
