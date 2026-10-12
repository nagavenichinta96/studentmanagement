
import json
import os
class Student:
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "grade": self.grade
        }


class StudentManager:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = []
        self.load_students()

    def load_students(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    self.students = [
                        Student(
                            s["student_id"],
                            s["name"],
                            s["grade"]
                        )
                        for s in data
                    ]
            except (json.JSONDecodeError, KeyError):
                self.students = []

    def save_students(self):
        with open(self.filename, "w") as file:
            json.dump(
                [s.to_dict() for s in self.students],
                file,
                indent=4
            )

    def add_student(self):
        student_id = input("Enter Student ID: ").strip()

        if not student_id:
            print("Student ID cannot be empty.")
            return

        if any(s.student_id == student_id
               for s in self.students):
            print("Error: Student ID already exists!")
            return

        name = input("Enter Student Name: ").strip()
        grade = input("Enter Student Grade: ").strip()

        if not name or not grade:
            print("Name and grade cannot be empty.")
            return

        student = Student(student_id, name, grade)
        self.students.append(student)
        self.save_students()
        print("Student added successfully!")

    def list_students(self):
        if not self.students:
            print("No student records found.")
            return

        print("\n" + "-" * 55)
        print(f"{'ID':<12}{'NAME':<25}{'GRADE':<15}")
        print("-" * 55)

        for s in self.students:
            print(f"{s.student_id:<12}"
                  f"{s.name:<25}{s.grade:<15}")

        print("-" * 55)

    def search_student(self):
        student_id = input("Enter Student ID to search: ").strip()

        for s in self.students:
            if s.student_id == student_id:
                print("ID:", s.student_id)
                print("Name:", s.name)
                print("Grade:", s.grade)
                return

        print("Student not found.")

    def update_student(self):
        student_id = input("Enter Student ID to update: ").strip()

        for s in self.students:
            if s.student_id == student_id:
                name = input("Enter new name (blank to keep current): ").strip()
                grade = input("Enter new grade (blank to keep current): ").strip()

                if name:
                    s.name = name
                if grade:
                    s.grade = grade

                self.save_students()
                print("Student updated successfully!")
                return

        print("Student not found.")

    def delete_student(self):
        student_id = input("Enter Student ID to delete: ").strip()

        for s in self.students:
            if s.student_id == student_id:
                self.students.remove(s)
                self.save_students()
                print("Student deleted successfully!")
                return

        print("Student not found.")


def main():
    manager = StudentManager()

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. List Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            manager.add_student()
        elif choice == "2":
            manager.list_students()
        elif choice == "3":
            manager.search_student()
        elif choice == "4":
            manager.update_student()
        elif choice == "5":
            manager.delete_student()
        elif choice == "6":
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
