
import json
import os
class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.issued = False

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "issued": self.issued
        }


class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = {}
        self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)

                for item in data:
                    book = Book(
                        item["book_id"],
                        item["title"],
                        item["author"]
                    )
                    book.issued = item.get("issued", False)
                    self.books[book.book_id] = book

            except (json.JSONDecodeError, KeyError, TypeError):
                print("Warning: Could not load library data.")

    def save_books(self):
        with open(self.filename, "w") as file:
            json.dump(
                [book.to_dict() for book in self.books.values()],
                file,
                indent=4
            )

    def add_book(self):
        book_id = input("Enter Book ID: ").strip()

        if not book_id:
            print("Book ID cannot be empty.")
            return

        if book_id in self.books:
            print("Book ID already exists!")
            return

        title = input("Enter Book Title: ").strip()
        author = input("Enter Author Name: ").strip()

        if not title or not author:
            print("Title and author cannot be empty.")
            return

        book = Book(book_id, title, author)
        self.books[book_id] = book
        self.save_books()

        print("Book added successfully!")

    def display_books(self):
        if not self.books:
            print("No books available.")
            return

        print("\n" + "-" * 75)
        print(f"{'ID':<10}{'TITLE':<25}"
              f"{'AUTHOR':<22}{'STATUS':<12}")
        print("-" * 75)

        for book in self.books.values():
            status = "Issued" if book.issued else "Available"
            print(f"{book.book_id:<10}{book.title:<25}"
                  f"{book.author:<22}{status:<12}")

        print("-" * 75)

    def search_book(self):
        keyword = input("Enter title or author to search: ").strip().lower()

        results = [
            book for book in self.books.values()
            if keyword and (
                keyword in book.title.lower()
                or keyword in book.author.lower()
            )
        ]

        if results:
            print("\nSearch Results:")
            for book in results:
                status = "Issued" if book.issued else "Available"
                print(
                    f"ID: {book.book_id} | "
                    f"Title: {book.title} | "
                    f"Author: {book.author} | "
                    f"Status: {status}"
                )
        else:
            print("No matching books found.")

    def issue_book(self):
        book_id = input("Enter Book ID to issue: ").strip()

        if book_id not in self.books:
            print("Book not found.")
            return

        book = self.books[book_id]

        if book.issued:
            print("This book is already issued.")
            return

        book.issued = True
        self.save_books()
        print("Book issued successfully!")

    def return_book(self):
        book_id = input("Enter Book ID to return: ").strip()

        if book_id not in self.books:
            print("Book not found.")
            return

        book = self.books[book_id]

        if not book.issued:
            print("This book has not been issued.")
            return

        book.issued = False
        self.save_books()
        print("Book returned successfully!")

    def reports(self):
        total = len(self.books)
        issued = sum(
            1 for book in self.books.values()
            if book.issued
        )
        available = total - issued

        print("\n===== LIBRARY REPORT =====")
        print("Total books     :", total)
        print("Issued books    :", issued)
        print("Available books :", available)


def main():
    library = Library()

    while True:
        print("\n===== LIBRARY BOOK INVENTORY MANAGER =====")
        print("1. Add Book")
        print("2. Display All Books")
        print("3. Search Book")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. View Reports")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            library.add_book()
        elif choice == "2":
            library.display_books()
        elif choice == "3":
            library.search_book()
        elif choice == "4":
            library.issue_book()
        elif choice == "5":
            library.return_book()
        elif choice == "6":
            library.reports()
        elif choice == "7":
            print("Thank you for using the Library Manager!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
