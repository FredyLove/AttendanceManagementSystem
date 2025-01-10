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