import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# File to store database
DB_FILE = "students.json"

# Load database if it exists
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        students_db = json.load(f)
else:
    students_db = {}

def save_database():
    """Save the student database to a JSON file"""
    with open(DB_FILE, "w") as f:
        json.dump(students_db, f, indent=4)

def get_rank(points):
    """Return performance rank based on average points"""
    if points >= 80:
        return "🏆 Excellent"
    elif points >= 60:
        return "👍 Good"
    elif points >= 40:
        return "🙂 Average"
    else:
        return "⚠️ Needs Improvement"

def get_grade(points):
    """Return grade based on average points"""
    if 80 <= points <= 100:
        return "A"
    elif 75 <= points <= 79:
        return "A-"
    elif 70 <= points <= 74:
        return "B+"
    elif 65 <= points <= 69:
        return "B"
    elif 60 <= points <= 64:
        return "B-"
    elif 55 <= points <= 59:
        return "C+"
    elif 50 <= points <= 54:
        return "C"
    elif 40 <= points <= 49:
        return "C-"
    elif 35 <= points <= 39:
        return "D+"
    elif 30 <= points <= 34:
        return "D"
    elif 25 <= points <= 29:
        return "D-"
    else:
        return "E"

def add_student():
    name = simpledialog.askstring("Student Name", "Enter student name:")
    if not name:
        return

    subjects = {}
    compulsory = ["Maths", "English", "Kiswahili", "Biology", "Chemistry", "Physics"]

    for sub in compulsory:
        mark = simpledialog.askinteger("Input Marks", f"Enter marks for {sub}:")
        if mark is None:
            return
        subjects[sub] = mark

    # Optional Group 1
    group1 = ["Computer Studies", "Agriculture", "Music", "German"]
    choice1 = simpledialog.askstring("Optional Subject 1", f"Choose one: {', '.join(group1)}")
    if choice1 not in group1:
        messagebox.showerror("Error", "Invalid choice. Please restart.")
        return
    mark1 = simpledialog.askinteger("Input Marks", f"Enter marks for {choice1}:")
    subjects[choice1] = mark1

    # Optional Group 2
    group2 = ["History", "Geography"]
    choice2 = simpledialog.askstring("Optional Subject 2", f"Choose one: {', '.join(group2)}")
    if choice2 not in group2:
        messagebox.showerror("Error", "Invalid choice. Please restart.")
        return
    mark2 = simpledialog.askinteger("Input Marks", f"Enter marks for {choice2}:")
    subjects[choice2] = mark2

    total_marks = sum(subjects.values())
    total_points = total_marks / 8
    rank = get_rank(total_points)
    grade = get_grade(total_points)

    students_db[name] = {
        "Subjects": subjects,
        "Total Marks": total_marks,
        "Average Points": total_points,
        "Rank": rank,
        "Grade": grade
    }

    save_database()

    result = f"=== Results for {name} ===\n"
    for subject, mark in subjects.items():
        result += f"{subject}: {mark}\n"
    result += f"\nTotal Marks: {total_marks}\nAverage Points: {total_points:.2f}\nRank: {rank}\nGrade: {grade}"

    messagebox.showinfo("Student Results", result)

def view_all_students():
    if not students_db:
        messagebox.showinfo("Database", "No students added yet.")
        return

    result = "=== All Students ===\n"
    for name, data in students_db.items():
        result += f"\n{name} - Avg: {data['Average Points']:.2f} - {data['Rank']} - Grade: {data['Grade']}"
    messagebox.showinfo("All Students", result)

def view_student():
    if not students_db:
        messagebox.showinfo("Database", "No students added yet.")
        return

    name = simpledialog.askstring("Search Student", "Enter student name:")
    if name in students_db:
        data = students_db[name]
        result = f"=== Results for {name} ===\n"
        for subject, mark in data["Subjects"].items():
            result += f"{subject}: {mark}\n"
        result += f"\nTotal Marks: {data['Total Marks']}\nAverage Points: {data['Average Points']:.2f}\nRank: {data['Rank']}\nGrade: {data['Grade']}"
        messagebox.showinfo("Student Result", result)
    else:
        messagebox.showerror("Not Found", f"No student found with name '{name}'")

# Tkinter GUI
root = tk.Tk()
root.title("Student Results Manager")
root.geometry("350x320")

add_btn = tk.Button(root, text="➕ Add Student", command=add_student, width=25, height=2)
add_btn.pack(pady=10)

view_btn = tk.Button(root, text="📋 View All Students", command=view_all_students, width=25, height=2)
view_btn.pack(pady=10)

search_btn = tk.Button(root, text="🔎 View Individual Student", command=view_student, width=25, height=2)
search_btn.pack(pady=10)

exit_btn = tk.Button(root, text="❌ Exit", command=root.quit, width=25, height=2, bg="red", fg="white")
exit_btn.pack(pady=10)

root.mainloop()