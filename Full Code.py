import sqlite3
from datetime import datetime

###################################### SQL connection & Database Creation ######################################
# Connect to SQLite database
conn = sqlite3.connect('SchoolDatabase.db') 
# Function to create the database tables if they don't exist
def create_tables():
    conn.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    grade INTEGER NOT NULL,
                    enrollement_date TEXT,
                    data_entry_date DATE)''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS lessons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    name TEXT NOT NULL)''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS student_lessons (
                    student_id INTEGER,
                    lesson_id INTEGER,
                    FOREIGN KEY (student_id) REFERENCES students(id),
                    FOREIGN KEY (lesson_id) REFERENCES lessons(id),
                    PRIMARY KEY (student_id, lesson_id))''')

############################################## Student Functions ##############################################
## F1: Add Student
def add_student():
    while True:
        id_input = input("Enter student id: ").strip()
        if id_input == "":
            print("Student ID cannot be empty. Please enter a valid student ID.")
            continue
        try:
            id = int(id_input)
            break  # If conversion is successful and input isn't empty, exit the loop
        except ValueError:
            print("Invalid input. Please enter a valid integer for the student ID.")

    # Check if student ID already exists
    existing_id = conn.execute("SELECT id FROM students WHERE id = ?", (id,)).fetchone()
    if existing_id:
        
        print("A student with this ID already exists. Please try again with a different ID.")
        return

    first_name = input("Enter first name: ").strip()
    while any(char.isdigit() for char in first_name) or first_name == "":
        if first_name == "":
            print("First name cannot be empty.")
        else:
            
            print("First name cannot contain numbers. Please enter again.")
        first_name = input("Enter first name: ").strip()

    last_name = input("Enter last name: ").strip()
    while any(char.isdigit() for char in last_name) or last_name == "":
        if last_name == "":
            print("Last name cannot be empty.")
        else:
            print("Last name cannot contain numbers. Please enter again.")
        last_name = input("Enter last name: ").strip()

    while True:
        age_input = input("Enter age: ").strip()
        try:
            age = int(age_input)
            if age < 5 or age > 19:
                raise ValueError("Age must be between 5 and 19.")
            break  # Exit loop if age is valid
        except ValueError:
            print("Invalid input. Age must be a number between 5 and 19. Please enter again.")

    while True:
        try:
            grade_input = input("Enter grade: ").strip()
            grade = int(grade_input)  # Attempt to convert the input to an integer
            valid_grades = [i for i in range(1, 13)]  # Assuming grades are 1 through 12
            if grade not in valid_grades:
                raise ValueError("Grade must be between 1 and 12. Please enter again.")
            break  # Exit the loop if input is valid
        except ValueError:
            print("Invalid input. Grade must be an integer between 1 and 12.")


    def valid_date_format(date_input):
        try:
            datetime.strptime(date_input, '%Y-%m-%d')
            return True
        except ValueError:
            return False
        
    enrollement_date = input("Enter enrollement date (YYYY-MM-DD): ").strip()
    while not valid_date_format(enrollement_date):
        if enrollement_date == "":
            print("Enrollment date cannot be empty.")
        else:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        enrollement_date = input("Enter enrollment date (YYYY-MM-DD): ").strip()

    data_entry_date = datetime.now().strftime('%Y-%m-%d')

    conn.execute("INSERT INTO students (id, first_name, last_name, age, grade, enrollement_date, data_entry_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                 (id, first_name, last_name, age, grade, enrollement_date, data_entry_date))
    conn.commit()
    print("Student added successfully!")

    # Assign lesson/s to the last added student
    # Check for the availability of lessons
    lessons = conn.execute("SELECT id, name FROM lessons").fetchall()
    if not lessons:
        print("There are no available lessons now. Add a lesson first, then use the assign lesson function to assign lessons to the student you just added.")
        return  # Exit the function since there are no lessons to assign
    # Display all available lessons
    print("Select lessons to enroll the student in. Available lessons are:")
    for lesson in lessons:
        print(f"{lesson[0]}: {lesson[1]}")

    selected_lessons = []
    lesson_count = int(input("How many lessons is the student enrolled in? ").strip())

    for i in range(lesson_count):
        while True:
            lesson_id_input = input(f"Enter the ID of lesson {i+1} to assign to the student, or type 'done' to finish: ").strip()
            if lesson_id_input.lower() == 'done':
                break
            try:
                lesson_id = int(lesson_id_input)
                if lesson_id in [lesson[0] for lesson in lessons]:
                    selected_lessons.append(lesson_id)
                    print(f"Lesson with ID {lesson_id} is selected.")
                    break
                else:
                    print("Invalid lesson ID. Please select a valid ID from the list.")
            except ValueError:
                print("Please enter a valid numeric ID.")
        
        if lesson_id_input.lower() == 'done':
            break

    for lesson_id in selected_lessons:
        # Assign the lesson to the student
        conn.execute("INSERT INTO student_lessons (student_id, lesson_id) VALUES (?, ?)", (id, lesson_id))
        conn.commit()
    print("Lessons assigned successfully.") 

## F2 : list all students
def list_students():
    print("=== List of Students ===")
    try:
        students = conn.execute("SELECT id, first_name, last_name FROM students ORDER BY id ASC").fetchall()
        if students:
            for student in students:
                print(f"ID: {student[0]}, First Name: {student[1]}, Last Name: {student[2]}")
        else:
            print("No students found.")
    except Exception as e:
        print(f"An error occurred: {e}")

## F3 : Display student info
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
        
        print("Student not found!")

## F4: Modify student   
def modify_student():
    student_id_input = input("Enter student ID to modify: ").strip()
    try:
        student_id = int(student_id_input)
    except ValueError:
        print("Invalid input. Please enter a valid integer for the student ID.")
        return
    
    # Check if student exists
    check = conn.execute("SELECT COUNT(*) FROM students WHERE id = ?", (student_id,)).fetchone()
    if check[0] == 0:
        print("Student not found!")
        return

    new_first_name = input("Enter new first name (press Enter to skip): ").strip()
    while any(char.isdigit() for char in new_first_name) and new_first_name:
        print("First name cannot contain numbers. Please enter again.")
        new_first_name = input("Enter new first name: ").strip()

    new_last_name = input("Enter new last name (press Enter to skip): ").strip()
    while any(char.isdigit() for char in new_last_name) and new_last_name:
        print("Last name cannot contain numbers. Please enter again.")
        new_last_name = input("Enter new last name: ").strip()

    new_age = input("Enter new age (press Enter to skip): ").strip()
    if new_age:
        try:
            new_age = int(new_age)
            while new_age < 5 or new_age > 19:
                print("Age must be between 5 and 19. Please enter again.")
                new_age = int(input("Enter new age: ").strip())
        except ValueError:
            print("Invalid input. Age must be a number.")
            return

    new_grade = input("Enter new grade (press Enter to skip): ").strip()
    if new_grade:
        try:
            new_grade = int(new_grade)
            valid_grades = [i for i in range(1, 13)]
            if new_grade not in valid_grades:
                print("Invalid grade. Grade must be between 1 and 12.")
                return
        except ValueError:
            print("Invalid input. Grade must be a number.")
            return

    if new_first_name:
        conn.execute("UPDATE students SET first_name = ? WHERE id = ?", (new_first_name, student_id))
    if new_last_name:
        conn.execute("UPDATE students SET last_name = ? WHERE id = ?", (new_last_name, student_id))
    if new_age:
        conn.execute("UPDATE students SET age = ? WHERE id = ?", (new_age, student_id))
    if new_grade:
        conn.execute("UPDATE students SET grade = ? WHERE id = ?", (new_grade, student_id))

    conn.commit()
    print("Student information modified successfully!")

## F5: Delete student   
def delete_student():
    student_id_input = input("Enter student ID to delete: ").strip()
    try:
        student_id = int(student_id_input)  # Convert input to integer
    except ValueError:
        print("Invalid input. Please enter a valid integer for the student ID.")
        return  # Exit the function if input is not a valid integer

    # Check if the student exists before attempting to delete
    existing_student = conn.execute("SELECT id FROM students WHERE id = ?", (student_id,)).fetchone()
    if not existing_student:
        print("No student found with the provided ID.")
        return  # Exit the function if no student is found

    # Ask for confirmation before deleting
    confirmation = input("Are you sure you want to delete this student and all his/her related lessons? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.execute("DELETE FROM student_lessons WHERE student_id = ?", (student_id,))
        conn.commit()
        print("Student and his/her related lessons deleted successfully!!")
    else:
        print("Student deletion cancelled.")

############################################## Lesson Functions ##############################################
## F1: Add lesson
def add_lesson():
    display_lessons()
    while True:
        lesson_name = input("Enter the new lesson name: ").strip()
        # Check if name is empty or numeric-only
        if not lesson_name:
            print("Lesson name cannot be empty. Please enter a valid lesson name.")
        elif lesson_name.isdigit():
            print("Lesson name cannot be purely numeric. Please enter a valid lesson name.")
        else:
            break  # Proceed if name is valid

    # Check for lesson name uniqueness
    existing_lesson = conn.execute("SELECT name FROM lessons WHERE name = ?", (lesson_name,)).fetchone()
    if existing_lesson:
        print("This lesson already exists.")
        return
    conn.execute("INSERT INTO lessons (name) VALUES (?)", (lesson_name,))
    conn.commit()
    print("Lesson added successfully.")

## F2: Display lesson
def display_lessons():
    print("Available Lessons:")
    lessons = conn.execute("SELECT id, name FROM lessons").fetchall()
    if not lessons:
        print("No lessons available.")
        return
    for lesson in lessons:
        print(f"ID: {lesson[0]}, Name: {lesson[1]}")

## F3: Modify lesson
def modify_lesson():
    display_lessons() 
    lesson_id_input = input("Enter the lesson ID to modify: ").strip()
    try:
        lesson_id = int(lesson_id_input)
    except ValueError:
        print("Invalid input. Please enter a valid integer for the lesson ID.")
        return

    # Check if the lesson exists
    existing_lesson = conn.execute("SELECT id FROM lessons WHERE id = ?", (lesson_id,)).fetchone()
    if not existing_lesson:
        print("This lesson does not exist.")
        return

    while True:
        new_name = input("Enter the new name for the lesson: ").strip()
        if not new_name:
            print("Lesson name cannot be empty. Please enter a valid name.")
            continue
        if new_name.isdigit():
            print("Lesson name cannot be purely numeric. Please enter a valid name.")
            continue
        break

    conn.execute("UPDATE lessons SET name = ? WHERE id = ?", (new_name, lesson_id))
    conn.commit()
    print("Lesson modified successfully.")

## F4: Assign lesson
def assign_lessons():
    # Display all available lessons
    print("Select lessons to enroll the student in. Available lessons are:")
    lessons = conn.execute("SELECT id, name FROM lessons").fetchall()
    for lesson in lessons:
        print(f"{lesson[0]}: {lesson[1]}")

    # Prompt for and validate the student ID
    student_id_input = input("Enter the student ID you want to assign the lesson/s to: ").strip()
    try:
        student_id = int(student_id_input)
    except ValueError:
        print("Invalid input. Please enter a valid integer for the student ID.")
        return

    # Check if the student exists in the database
    check = conn.execute("SELECT COUNT(*) FROM students WHERE id = ?", (student_id,)).fetchone()
    if check[0] == 0:
        print("Student not found!")
        return

    # Display lessons the student is already enrolled in
    enrolled_lessons = conn.execute("SELECT lessons.id FROM student_lessons JOIN lessons ON student_lessons.lesson_id = lessons.id WHERE student_lessons.student_id = ?", (student_id,)).fetchall()
    enrolled_lesson_ids = [lesson[0] for lesson in enrolled_lessons]
    if enrolled_lessons:
        print("This student is currently enrolled in the following lessons:")
        for lesson_id in enrolled_lesson_ids:
            print(f"Lesson ID: {lesson_id}")
    else:
        print("This student is not enrolled in any lessons.")

    # Ask how many additional lessons the student is to be enrolled in
    lesson_count = int(input("How many additional lessons is the student to be enrolled in? "))
    enrolled_count = 0  # Track the number of successfully enrolled lessons
    while enrolled_count < lesson_count:
        lesson_id_input = input("Enter the ID of the lesson to assign to the student, or type 'done' to finish: ").strip()
        if lesson_id_input.lower() == 'done' or not lesson_id_input:
            if not lesson_id_input:  # Handle empty input by prompting the user again without exiting
                print("No input detected. Please enter a valid lesson ID or type 'done' to finish.")
                continue
            print("Ending lesson assignment process.")
            break

        try:
            lesson_id = int(lesson_id_input)
            if lesson_id not in [lesson[0] for lesson in lessons]:
                print("Invalid lesson ID. Please select a valid ID from the list.")
                continue

            if lesson_id in enrolled_lesson_ids:
                print(f"Student is already enrolled in lesson with ID {lesson_id}.")
                continue

            # Insert the new lesson for the student in the database
            conn.execute("INSERT INTO student_lessons (student_id, lesson_id) VALUES (?, ?)", (student_id, lesson_id))
            print(f"Lesson with ID {lesson_id} is selected.")
            enrolled_lesson_ids.append(lesson_id)  # Update enrolled lessons to reflect current state
            enrolled_count += 1  # Only increment count for successful enrollments
        except ValueError:
            print("Please enter a valid numeric ID.")

    # Commit the changes to the database
    conn.commit()
    print("Lessons assigned successfully.")

## F5: Delete lesson
def delete_lesson():
    display_lessons()
    lesson_id = input("Enter the lesson ID to delete: ").strip()
    try:
        lesson_id = int(lesson_id)
    except ValueError:
        print("Invalid input. Please enter a valid integer for the lesson ID.")
        return

    # Check if the lesson exists
    existing_lesson = conn.execute("SELECT id FROM lessons WHERE id = ?", (lesson_id,)).fetchone()
    if not existing_lesson:
        print("This lesson does not exist.")
        return
    
    # Ask for confirmation before deleting
    confirmation = input("Are you sure you want to delete this lesson? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        conn.execute("DELETE FROM lessons WHERE id = ?", (lesson_id,))
        conn.commit()
        print("Lesson deleted successfully.")
    else:
        print("Lesson deletion cancelled.")

################################################## MAIN MENU ##################################################
# Main function to run the program
def main():
    try:
        create_tables()
        while True:
            print("\n ***** Welcome to School Database CLI Program *****")
            print("Please choose the operation you want to perform:")
            print("=== Student-related operation ===")
            print("To add a student, press 'as'")
            print("To show the list of all students, press 'ss'")
            print("To view student information, press 'vs'")
            print("To modify student information, press 'ms'")
            print("To delete a student, press 'ds'")
            print("=== Lesson-related operation ===")
            print("To add a lesson, press 'al'")
            print("To view lessons list, press 'vl'")
            print("To modify lesson information, press 'ml'")
            print("To assign lessons to student, press 'als'")
            print("To delete a lesson, press 'dl'")
            print("=== To exit, press 'e' ===")

            choice = input("Your choice: ").lower()

            if choice == 'as':
                add_student()
            elif choice == 'ss':
                list_students()
            elif choice == 'vs':
                display_student()
            elif choice == 'ms':
                modify_student()
            elif choice == 'ds':
                delete_student()
            elif choice == 'al':
                add_lesson()
            elif choice == 'vl':
                display_lessons()
            elif choice == 'ml':
                modify_lesson()
            elif choice == 'als':
                assign_lessons()
            elif choice == 'dl':
                delete_lesson()
            elif choice == 'e':
                print("Exiting program...")
                break
            else:
                print("Invalid choice! Please try again.")
    finally:
        # Ensure the database connection is closed properly when the program is about to exit
        conn.close()

if __name__ == "__main__":
    main()