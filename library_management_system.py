import sqlite3

def setup_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
        isbn TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL,
        available INTEGER NOT NULL
    )''')
    conn.commit()
    conn.close()

class Library:
    @staticmethod
    def validate_book_details(isbn, title, author, year):
        """
        Validating the book details based on the constraints and collecting all errors.
        """
        errors = []

        if not isbn.isdigit():
            errors.append("ISBN must be a numeric value.")
        if not isinstance(title, str) or title.strip() == "":
            errors.append("Title must be a non-empty string.")
        if not isinstance(author, str) or any(char.isdigit() for char in author):
            errors.append("Author must be a string and should not contain digits.")
        if not str(year).isdigit() or not (1000 <= int(year) <= 9999):
            errors.append("Year must be a valid four-digit number.")

        return errors

    @staticmethod
    def add_book(isbn, title, author, year):
        """
        Adds a new book to the library database after validating constraints.
        If validation errors occur, they are printed.
        """
        # Validate the book details
        errors = Library.validate_book_details(isbn, title, author, year)
        if errors:
            print("Error(s) while adding the book:")
            for error in errors:
                print(f"- {error}")
            print("Book not added!!")
            return

        # Insert the book into the database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (isbn, title, author, year, available) VALUES (?, ?, ?, ?, ?)',
                       (isbn, title, author, year, 1))
        conn.commit()
        conn.close()
        print("Book added successfully.")

    @staticmethod
    def borrow_book(isbn):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT available FROM books WHERE isbn = ?', (isbn,))
        book = cursor.fetchone()
        if book and book[0] == 1:
            cursor.execute('UPDATE books SET available = 0 WHERE isbn = ?', (isbn,))
            conn.commit()
        else:
            conn.close()
            raise ValueError("Book is not available or does not exist.")
        conn.close()

    @staticmethod
    def return_book(isbn):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT available FROM books WHERE isbn = ?', (isbn,))
        book = cursor.fetchone()
        if book and book[0] == 0:
            cursor.execute('UPDATE books SET available = 1 WHERE isbn = ?', (isbn,))
            conn.commit()
        else:
            conn.close()
            raise ValueError("Book was not borrowed or does not exist.")
        conn.close()
    
    @staticmethod
    def view_available_books():
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT isbn, title, author, year FROM books WHERE available = 1')
        books = cursor.fetchall()
        conn.close()
        return books

def menu():
    setup_database()
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Borrow Book")
        print("3. Return Book")
        print("4. View Available Books")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            isbn = input("Enter ISBN: ")
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            year = input("Enter Year: ")
            Library.add_book(isbn, title, author, year)
        elif choice == "2":
            isbn = input("Enter ISBN to borrow: ")
            try:
                Library.borrow_book(isbn)
                print("Book borrowed successfully.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "3":
            isbn = input("Enter ISBN to return: ")
            try:
                Library.return_book(isbn)
                print("Book returned successfully.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "4":
            books = Library.view_available_books()
            print("Available Books:")
            for book in books:
                print(f"ISBN: {book[0]}, Title: {book[1]}, Author: {book[2]}, Year: {book[3]}")
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()

