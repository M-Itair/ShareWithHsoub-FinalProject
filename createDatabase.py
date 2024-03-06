import sqlite3
from datetime import datetime


# Connect to SQLite database
conn = sqlite3.connect('School_Database.db')

# Function to create the database tables if they don't exist
def create_tables():
    conn.execute('''CREATE TABLE IF NOT EXISTS students (
                    id TEXT PRIMARY KEY NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    grade TEXT NOT NULL,
                    enrollement_date TEXT,
                    data_entry_date DATE)''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS lessons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT)''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS student_lessons (
                    student_id TEXT,
                    lesson_name TEXT,
                    FOREIGN KEY (student_id) REFERENCES students(id),
                    FOREIGN KEY (lesson_name) REFERENCES lessons(name),
                    PRIMARY KEY (student_id, lesson_name))''')

# Function to add a student to the database
def add_student():
    id = input("Enter student id: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    age = int(input("Enter age: "))
    grade = input("Enter grade: ")
    enrollement_date = input("Enter enrollement date (YYYY-MM-DD): ")
    data_entry_date = datetime.now().strftime('%Y-%m-%d')

    conn.execute("INSERT INTO students (id, first_name, last_name, age, grade, enrollement_date, data_entry_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                 (id, first_name, last_name, age, grade, enrollement_date, data_entry_date))
    conn.commit()


    
    student_id = id


    lesson_count = int(input("How many lessons is the student enrolled in? "))
    for _ in range(lesson_count):
        lesson_name = input("Enter lesson name: ")

        # Check if lesson exists in the lessons table
        existing_lesson = conn.execute("SELECT id FROM lessons WHERE name = ?", (lesson_name,)).fetchone()
        if existing_lesson:
            pass
        else:
            # If lesson doesn't exist, insert it into the lessons table
            conn.execute("INSERT INTO lessons (name) VALUES (?)", (lesson_name,))
        
        conn.execute("INSERT INTO student_lessons (student_id, lesson_name) VALUES (?, ?)", (student_id, lesson_name))
        conn.commit()

    print("=== Operation Status ===")
    print("Student added successfully!")

# Function to delete a student from the database
def delete_student():
    student_id = input("Enter student ID to delete: ")
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.execute("DELETE FROM student_lessons WHERE student_id = ?", (student_id,))
    conn.commit()
    
    print("=== Operation Status ===")
    print("Student and his/her related lessons deleted successfully!!")

# Function to modify student information in the database
def modify_student():
    student_id = input("Enter student ID to modify: ")
    # Check if student exists
    if conn.execute("SELECT COUNT(*) FROM students WHERE id = ?", (student_id,)):
        print("=== Operation Status ===")
        print("Student not found!")
        return

    # Assuming we only allow modification of first name, last name, and grade for simplicity
    new_first_name = input("Enter new first name (press Enter to skip): ")
    new_last_name = input("Enter new last name (press Enter to skip): ")
    new_grade = input("Enter new grade (press Enter to skip): ")

    if new_first_name:
        conn.execute("UPDATE students SET first_name = ? WHERE id = ?", (new_first_name, student_id))
    if new_last_name:
        conn.execute("UPDATE students SET last_name = ? WHERE id = ?", (new_last_name, student_id))
    if new_grade:
        conn.execute("UPDATE students SET grade = ? WHERE id = ?", (new_grade, student_id))

    conn.commit()
    print("=== Operation Status ===")
    print("Student information modified successfully!")

# Function to display student information
def display_student():
    student_id = input("Enter student ID to display information: ")
    student_info = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if student_info:
        print("Student ID:", student_info[0])
        print("First Name:", student_info[1])
        print("Last Name:", student_info[2])
        print("Age:", student_info[3])
        print("Grade:", student_info[4])
        print("Enrollement Date:", student_info[5])
        print("Data Entry Date:", student_info[6])


        # Fetch and display enrolled lessons
        lessons = conn.execute("SELECT lesson_name FROM student_lessons WHERE student_id = ?", (student_id,)).fetchall()
        if lessons:
            print("Enrolled Lessons:")
            for lesson in lessons:
                print("- ", lesson[0])
        else:
            print("No lessons enrolled for this student.")
    else:
        print("=== Operation Status ===")
        print("Student not found!")

# Main function to run the program
def main():
    create_tables()

    while True:
        print("\n Please choose the operation you want to perform:")
        print("To add a student, press 'a'")
        print("To delete a student, press 'd'")
        print("To modify student information, press 'm'")
        print("To view student information, press 'v'")
        print("To exit, press 'e'")

        choice = input("Your choice: ").lower()

        if choice == 'a':
            add_student()
        elif choice == 'd':
            delete_student()
        elif choice == 'm':
            modify_student()
        elif choice == 'v':
            display_student()
        elif choice == 'e':
            print("=== Operation Status ===")
            print("Exiting program...")
            break
        else:
            print("=== Operation Status ===")
            print("Invalid choice! Please try again.")



if __name__ == "__main__":
    main()