import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import backend

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c2f36") 

        # Header
        title = tk.Label(self.root, text="Attendance Management System", font=("Arial", 20, "bold"), fg="white", bg="#2c2f36")
        title.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#2c2f36")
        btn_frame.pack(pady=10)

        self.import_btn = ttk.Button(btn_frame, text="Import Class List", command=self.import_class_list, style="TButton")
        self.import_btn.grid(row=0, column=0, padx=5)

        self.create_list_btn = ttk.Button(btn_frame, text="Create Class List", command=self.create_class_list, style="TButton")
        self.create_list_btn.grid(row=0, column=1, padx=5)

        self.mark_attendance_btn = ttk.Button(btn_frame, text="Mark Attendance", command=self.mark_attendance, style="TButton")
        self.mark_attendance_btn.grid(row=0, column=2, padx=5)

        self.add_marks_btn = ttk.Button(btn_frame, text="Add/Deduct Marks", command=self.add_deduct_marks, style="TButton")
        self.add_marks_btn.grid(row=0, column=3, padx=5)

        self.view_stats_btn = ttk.Button(btn_frame, text="View Attendance Stats", command=self.view_stats, style="TButton")
        self.view_stats_btn.grid(row=0, column=4, padx=5)

        # Delete Student Button
        self.delete_btn = ttk.Button(btn_frame, text="Delete Student", command=self.delete_student, style="TButton")
        self.delete_btn.grid(row=0, column=5, padx=5)

        # Delete Class List Button
        self.delete_class_btn = ttk.Button(self.root, text="Delete Class List", command=self.delete_class_list, style="TButton")
        self.delete_class_btn.pack(pady=10)

        # Table for displaying students with numbered names
        self.tree = ttk.Treeview(self.root, columns=("Number", "Name", "Attendance", "Marks"), show="headings", style="Treeview")
        self.tree.heading("Number", text="No.")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Attendance", text="Attendance")
        self.tree.heading("Marks", text="Marks")
        self.tree.column("Number", width=50, anchor="center")
        self.tree.column("Name", width=200, anchor="w")  # Left-align names
        self.tree.column("Attendance", width=100, anchor="center")
        self.tree.column("Marks", width=100, anchor="center")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        self.populate_table()

    def import_class_list(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel or Text Files", "*.xlsx;*.txt")])
        if file_path:
            success = backend.import_class_list(file_path)
            if success:
                messagebox.showinfo("Success", "Class list imported successfully!")
                self.populate_table()
            else:
                messagebox.showerror("Error", "Failed to import class list.")

    def create_class_list(self):
        def save_new_student():
            name = name_entry.get().strip()
            if name:
                backend.add_student(name)
                name_entry.delete(0, tk.END)
                self.populate_table()
            else:
                messagebox.showwarning("Warning", "Please enter a name!")

        # Create a new window for adding students
        new_window = tk.Toplevel(self.root)
        new_window.title("Create Class List")
        new_window.geometry("400x300")
        new_window.configure(bg="#2c2f36")

        tk.Label(new_window, text="Enter Student Name", font=("Arial", 12), bg="#2c2f36", fg="white").pack(pady=10)
        name_entry = ttk.Entry(new_window, width=30)
        name_entry.pack(pady=5)

        add_btn = ttk.Button(new_window, text="Add Student", command=save_new_student, style="TButton")
        add_btn.pack(pady=10)

        close_btn = ttk.Button(new_window, text="Close", command=new_window.destroy, style="TButton")
        close_btn.pack(pady=10)

    def delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a student to delete!")
            return

        student_name = self.tree.item(selected_item, "values")[1]
        confirm = messagebox.askyesno("Delete Student", f"Are you sure you want to delete {student_name}?")
        if confirm:
            backend.delete_student(student_name)
            self.populate_table()
            messagebox.showinfo("Success", f"Deleted {student_name}!")

    def delete_class_list(self):
        confirm = messagebox.askyesno("Delete Class List", "Are you sure you want to delete the entire class list?")
        if confirm:
            backend.clear_class_list()  # Function to clear the class list in the backend
            self.populate_table()
            messagebox.showinfo("Success", "Class list deleted successfully!")

    def mark_attendance(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a student!")
            return

        student_name = self.tree.item(selected_item, "values")[1]
        backend.mark_attendance(student_name)
        self.populate_table()
        messagebox.showinfo("Success", f"Marked attendance for {student_name}!")

    def add_deduct_marks(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a student!")
            return

        student_name = self.tree.item(selected_item, "values")[1]

        def update_marks():
            try:
                marks = int(marks_entry.get().strip())
                backend.update_marks(student_name, marks)
                self.populate_table()
                marks_window.destroy()
                messagebox.showinfo("Success", f"Updated marks for {student_name} by {marks} points!")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number!")

        # Create a window to enter marks
        marks_window = tk.Toplevel(self.root)
        marks_window.title("Add/Deduct Marks")
        marks_window.geometry("300x200")
        marks_window.configure(bg="#2c2f36")

        tk.Label(marks_window, text=f"Student: {student_name}", font=("Arial", 12), bg="#2c2f36", fg="white").pack(pady=10)
        tk.Label(marks_window, text="Enter marks to add/deduct (+/-):", font=("Arial", 12), bg="#2c2f36", fg="white").pack(pady=5)
        marks_entry = ttk.Entry(marks_window, width=20)
        marks_entry.pack(pady=5)

        submit_btn = ttk.Button(marks_window, text="Update Marks", command=update_marks, style="TButton")
        submit_btn.pack(pady=10)

    def view_stats(self):
        stats = backend.get_stats()
        if stats:
            # Create a new window for displaying the stats
            stats_window = tk.Toplevel(self.root)
            stats_window.title("Attendance Stats")
            stats_window.geometry("600x400")
            stats_window.configure(bg="#2c2f36")

            stats_tree = ttk.Treeview(stats_window, columns=("Name", "Attendance"), show="headings", style="Treeview")
            stats_tree.heading("Name", text="Name")
            stats_tree.heading("Attendance", text="Attendance")
            stats_tree.column("Name", width=200, anchor="w")
            stats_tree.column("Attendance", width=100, anchor="center")
            stats_tree.pack(pady=10, fill=tk.BOTH, expand=True)

            for name, attendance in stats.items():
                stats_tree.insert("", "end", values=(name, attendance))

        else:
            messagebox.showinfo("Attendance Stats", "No attendance records found!")

    def populate_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        students = backend.get_students()
        if not students:
            messagebox.showinfo("Info", "No class list found! You can create one.")
        # Sorting students alphabetically by name
        students.sort(key=lambda student: student["name"].lower())
        for index, student in enumerate(students, start=1):
            self.tree.insert("", "end", values=(index, student["name"], student["attendance"], student["marks"]))


if __name__ == "__main__":
    root = tk.Tk()

    # Style Configuration
    style = ttk.Style()
    style.configure("TButton", 
                    background="#007bff",  
                    foreground="black", 
                    font=("Arial", 12), 
                    padding=10) 

    style.map("TButton", 
              background=[('active', '#0056b3')])  

    style.configure("Treeview", 
                    font=("Arial", 12), 
                    background="#3e3e3e", 
                    foreground="white", 
                    rowheight=25)
    style.configure("Treeview.Heading", 
                    font=("Arial", 14, "bold"), 
                    background="#4CAF50", 
                    foreground="black")

    app = AttendanceApp(root)
    root.mainloop()
