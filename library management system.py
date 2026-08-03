# library management system 

import sqlite3
from datetime import datetime, timedelta

class LibraryDatabase:
    """Handles database connections and SQL operations."""
    def __init__(self, db_name="library.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Books Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                total_copies INTEGER NOT NULL,
                available_copies INTEGER NOT NULL
            )
        ''')
        # Members Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        # Issued Books Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS issued_books (
                issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                member_id INTEGER,
                issue_date TEXT,
                return_date TEXT,
                status TEXT DEFAULT 'ISSUED',
                FOREIGN KEY(book_id) REFERENCES books(book_id),
                FOREIGN KEY(member_id) REFERENCES members(member_id)
            )
        ''')
        self.conn.commit()

    def close(self):
        self.conn.close()


class LibrarySystem:
    """Handles business logic for the Library Management System."""
    def __init__(self, db):
        self.db = db

    def add_book(self, title, author, copies):
        self.db.cursor.execute(
            "INSERT INTO books (title, author, total_copies, available_copies) VALUES (?, ?, ?, ?)",
            (title, author, copies, copies)
        )
        self.db.conn.commit()
        print(f"\n✅ Book '{title}' added successfully!")

    def register_member(self, name):
        self.db.cursor.execute("INSERT INTO members (name) VALUES (?)", (name,))
        self.db.conn.commit()
        member_id = self.db.cursor.lastrowid
        print(f"\n✅ Member registered successfully! ID: {member_id}")

    def display_books(self):
        self.db.cursor.execute("SELECT * FROM books")
        books = self.db.cursor.fetchall()
        print("\n" + "="*50)
        print("LIBRARY BOOKS CATALOG".center(50))
        print("="*50)
        if not books:
            print("No books currently in the library.")
            return

        print(f"{'ID':<5} {'Title':<25} {'Author':<15} {'Available/Total'}")
        print("-" * 50)
        for b in books:
            print(f"{b[0]:<5} {b[1]:<25} {b[2]:<15} {b[4]}/{b[3]}")

    def issue_book(self, book_id, member_id):
        # Check if book exists and is available
        self.db.cursor.execute("SELECT available_copies, title FROM books WHERE book_id = ?", (book_id,))
        book = self.db.cursor.fetchone()

        if not book:
            print("\n❌ Error: Book ID not found.")
            return
        if book[0] <= 0:
            print(f"\n❌ Sorry, all copies of '{book[1]}' are currently checked out.")
            return

        # Check if member exists
        self.db.cursor.execute("SELECT name FROM members WHERE member_id = ?", (member_id,))
        member = self.db.cursor.fetchone()
        if not member:
            print("\n❌ Error: Member ID not found.")
            return

        issue_date = datetime.now().strftime("%Y-%m-%d")
        return_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d") # 14-day loan

        # Log issued book
        self.db.cursor.execute(
            "INSERT INTO issued_books (book_id, member_id, issue_date, return_date) VALUES (?, ?, ?, ?)",
            (book_id, member_id, issue_date, return_date)
        )
        # Decrease available copy count
        self.db.cursor.execute(
            "UPDATE books SET available_copies = available_copies - 1 WHERE book_id = ?",
            (book_id,)
        )
        self.db.conn.commit()
        print(f"\n✅ Successfully issued '{book[1]}' to {member[0]}. Due Date: {return_date}")

    def return_book(self, issue_id):
        self.db.cursor.execute(
            "SELECT book_id, status FROM issued_books WHERE issue_id = ?", (issue_id,)
        )
        record = self.db.cursor.fetchone()

        if not record:
            print("\n❌ Error: Issue Record ID not found.")
            return
        if record[1] == 'RETURNED':
            print("\n❌ Error: This book has already been returned.")
            return

        book_id = record[0]
        # Mark as returned
        self.db.cursor.execute(
            "UPDATE issued_books SET status = 'RETURNED' WHERE issue_id = ?", (issue_id,)
        )
        # Increase available copy count
        self.db.cursor.execute(
            "UPDATE books SET available_copies = available_copies + 1 WHERE book_id = ?",
            (book_id,)
        )
        self.db.conn.commit()
        print(f"\n✅ Book returned successfully!")


# Interactive CLI Menu
def main():
    db = LibraryDatabase()
    system = LibrarySystem(db)

    while True:
        print("\n--- 📚 LIBRARY MANAGEMENT MENU ---")
        print("1. Display All Books")
        print("2. Add New Book")
        print("3. Register New Member")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == '1':
            system.display_books()
        elif choice == '2':
            title = input("Enter book title: ")
            author = input("Enter author: ")
            copies = int(input("Enter number of copies: "))
            system.add_book(title, author, copies)
        elif choice == '3':
            name = input("Enter member name: ")
            system.register_member(name)
        elif choice == '4':
            book_id = int(input("Enter Book ID to issue: "))
            member_id = int(input("Enter Member ID: "))
            system.issue_book(book_id, member_id)
        elif choice == '5':
            issue_id = int(input("Enter Issue Transaction ID: "))
            system.return_book(issue_id)
        elif choice == '6':
            print("\nExiting system. Goodbye!")
            db.close()
            break
        else:
            print("\n❌ Invalid choice! Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()