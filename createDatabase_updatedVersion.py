import sqlite3
from datetime import datetime


# Connect to SQLite database
conn = sqlite3.connect('schoolDatabase.db') 

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
                    lesson_id TEXT,
                    FOREIGN KEY (student_id) REFERENCES students(id),
                    FOREIGN KEY (lesson_id) REFERENCES lessons(id),
                    PRIMARY KEY (student_id, lesson_id))''')


###################### STUDENT FUNCTIONS() ######################
# Function to add a student to the database with input validaiton
def add_student():
    id = input("Enter student id: ")
    # Check if student ID already exists
    existing_id = conn.execute("SELECT id FROM students WHERE id = ?", (id,)).fetchone()
    if existing_id:
        print("=== Operation Status ===")
        print("A student with this ID already exists. Please try again with a different ID.")
        return

    first_name = input("Enter first name: ")
    while any(char.isdigit() for char in first_name):
        print("First name cannot contain numbers. Please enter again.")
        first_name = input("Enter first name: ")

    last_name = input("Enter last name: ")
    while any(char.isdigit() for char in last_name):
        print("Last name cannot contain numbers. Please enter again.")
        last_name = input("Enter last name: ")

    age = int(input("Enter age: "))
    while age < 5 or age > 19:
        print("Age must be between 5 and 19. Please enter again.")
        age = int(input("Enter age: "))

    grade = input("Enter grade: ")
    valid_grades = [str(i) for i in range(1, 13)]  # Assuming grades are 1 through 12
    while grade not in valid_grades:
        print("Grade must be between 1 and 12. Please enter again.")
        grade = input("Enter grade: ")

    enrollement_date = input("Enter enrollement date (YYYY-MM-DD): ")
    data_entry_date = datetime.now().strftime('%Y-%m-%d')

    conn.execute("INSERT INTO students (id, first_name, last_name, age, grade, enrollement_date, data_entry_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                 (id, first_name, last_name, age, grade, enrollement_date, data_entry_date))
    conn.commit()

    print("=== Operation Status ===")
    print("Student added successfully!")

    lesson_count = int(input("How many lessons is the student enrolled in? "))
    for i in range(lesson_count):
        print("=== Operation Status ===")
        print(f"Adding lesson {i+1} of {lesson_count}")

        # Display all available lessons
        print("Select lessons to enroll the student in. Available lessons are:")
        lessons = conn.execute("SELECT id, name FROM lessons").fetchall()
        for lesson in lessons:
            print(f"{lesson[0]}: {lesson[1]}")
    
        lesson_name = input("Enter the lesson name to assign to the student (or type 'done' to finish): ")
        if lesson_name.lower() == 'done':
            break
        
        # Check if the lesson exists, and add it if not
        lesson = conn.execute("SELECT id FROM lessons WHERE name = ?", (lesson_name,)).fetchone()
        if lesson:
                lesson_id = lesson[0]
                print(f"Lesson {lesson_name} is selected")
        else:
            print(f"Lesson '{lesson_name}' not found. Adding new lesson.")
            cursor = conn.execute("INSERT INTO lessons (name) VALUES (?)", (lesson_name,))
            conn.commit()
            lesson_id = cursor.lastrowid
            print(f"Lesson '{lesson_name}' added with ID {lesson_id}.")

        # Assign the lesson to the student
        conn.execute("INSERT INTO student_lessons (student_id, lesson_id) VALUES (?, ?)", (id, lesson_id))
        conn.commit()

    print("=== Operation Status ===")
    print("Lessons assigned successfully.")

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
    
    check = conn.execute("SELECT COUNT(*) FROM students WHERE id = ?", (student_id,)).fetchone()
    if check[0] == 0:
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
        lessons = conn.execute("""
            SELECT lessons.name 
            FROM lessons
            JOIN student_lessons ON lessons.id = student_lessons.lesson_id
            WHERE student_lessons.student_id = ?
            """, (student_id,)).fetchall()
        
        if lessons:
            print("Enrolled Lessons:")
            for lesson in lessons:
                print("- ", lesson[0])
        else:
            print("No lessons enrolled for this student.")
    else:
        print("=== Operation Status ===")
        print("Student not found!")


###################### LESSONS FUNCTIONS () ######################

def add_lesson():
    lesson_name = input("Enter the new lesson name: ")
    # Check for lesson name uniqueness
    existing_lesson = conn.execute("SELECT name FROM lessons WHERE name = ?", (lesson_name,)).fetchone()
    if existing_lesson:
        print("=== Operation Status ===")
        print("This lesson already exists.")
        return
    conn.execute("INSERT INTO lessons (name) VALUES (?)", (lesson_name,))
    conn.commit()
    print("=== Operation Status ===")
    print("Lesson added successfully.")

def display_lessons():
    print("Available Lessons:")
    lessons = conn.execute("SELECT id, name FROM lessons").fetchall()
    if not lessons:
        print("=== Operation Status ===")
        print("No lessons available.")
        return
    for lesson in lessons:
        print(f"ID: {lesson[0]}, Name: {lesson[1]}")

def delete_lesson():
    lesson_id = input("Enter the lesson ID to delete: ")
    # Check if the lesson exists
    existing_lesson = conn.execute("SELECT id FROM lessons WHERE id = ?", (lesson_id,)).fetchone()
    if not existing_lesson:
        print("=== Operation Status ===")
        print("This lesson does not exist.")
        return
    conn.execute("DELETE FROM lessons WHERE id = ?", (lesson_id,))
    conn.commit()
    print("=== Operation Status ===")
    print("Lesson deleted successfully.")

def modify_lesson():
    display_lessons()
    lesson_id = input("Enter the lesson ID to modify: ")
    new_name = input("Enter the new name for the lesson: ")
    # Check if the lesson exists
    existing_lesson = conn.execute("SELECT id FROM lessons WHERE id = ?", (lesson_id,)).fetchone()
    if not existing_lesson:
        print("=== Operation Status ===")
        print("This lesson does not exist")
        return
    conn.execute("UPDATE lessons SET name = ? WHERE id = ?", (new_name, lesson_id))
    conn.commit()
    print("=== Operation Status ===")
    print("Lesson modified successfully.")


###################### MAIN MENU ######################
# Main function to run the program
def main():
    try:
        create_tables()

        while True:
            print("\n Please choose the operation you want to perform:")
            print("=== Student-related operation ===")
            print("To add a student, press 'sa'")
            print("To delete a student, press 'sd'")
            print("To modify student information, press 'sm'")
            print("To view student information, press 'sv'")
            print("=== Lesson-related operation ===")
            print("To add a lesson, press 'la'")
            print("To delete a lesson, press 'ld'")
            print("To modify lesson information, press 'lm'")
            print("To view lessons list, press 'lv'")
            print("=== To exit, press 'e' ===")


            choice = input("Your choice: ").lower()

            if choice == 'sa':
                add_student()
            elif choice == 'sd':
                delete_student()
            elif choice == 'sm':
                modify_student()
            elif choice == 'sv':
                display_student()
            elif choice == 'la':
                add_lesson()
            elif choice == 'ld':
                delete_lesson()
            elif choice == 'lm':
                modify_lesson()
            elif choice == 'lv':
                display_lessons()
            elif choice == 'e':
                print("=== Operation Status ===")
                print("Exiting program...")
                break
            else:
                print("=== Operation Status ===")
                print("Invalid choice! Please try again.")
    finally:
        # Ensure the database connection is closed properly when the program is about to exit
        conn.close()


if __name__ == "__main__":
    main()