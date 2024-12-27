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
    def add_book(isbn, title, author, year):

        # Insert the book into the database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (isbn, title, author, year, available) VALUES (?, ?, ?, ?, ?)',
                       (isbn, title, author, year, 1))
        conn.commit()
        conn.close()
        print("Book added successfully.")

    @staticmethod
    def view_available_books():
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT isbn, title, author, year FROM books WHERE available = 1')
        books = cursor.fetchall()
        conn.close()
        return books
