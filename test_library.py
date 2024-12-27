import unittest
from library_management_system import Library, setup_database
import sqlite3

class TestLibrary(unittest.TestCase):
    """
    A class to test the Library Management System.
    """

    def setUp(self):
        """
        Setting up the test environment.
        """
        setup_database()
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books')  # Clear the books table before each test
        conn.commit()
        conn.close()

    def test_add_book(self):
        """
        Test for adding a valid book to the library.
        """
        Library.add_book("12345", "Test Book", "Author", 2023)
        books = Library.view_available_books()
        self.assertEqual(len(books), 1)  # Check if one book is added

    def test_add_book_invalid_details(self):
        """
        Test for adding a book with invalid details.
        """
        # Invalid ISBN (non-numeric)
        errors = Library.validate_book_details("12A45", "Test Book", "Author", 2023)
        self.assertIn("ISBN must be a numeric value.", errors)

        # Invalid title (empty string)
        errors = Library.validate_book_details("12345", "", "Author", 2023)
        self.assertIn("Title must be a non-empty string.", errors)

        # Invalid author (contains digits)
        errors = Library.validate_book_details("12345", "Test Book", "Author1", 2023)
        self.assertIn("Author must be a string and should not contain digits.", errors)

        # Invalid year (not a four-digit number)
        errors = Library.validate_book_details("12345", "Test Book", "Author", "20AB")
        self.assertIn("Year must be a valid four-digit number.", errors)

        # Multiple errors
        errors = Library.validate_book_details("12A45", "", "Author1", "20AB")
        self.assertEqual(len(errors), 4)  # All constraints violated

    def test_borrow_book(self):
        """
        Test for borrowing a book from the library.
        """
        Library.add_book("12345", "Test Book", "Author", 2023)
        Library.borrow_book("12345")
        books = Library.view_available_books()
        self.assertEqual(len(books), 0)  # Book is borrowed, so it should not be available

    def test_return_book(self):
        """
        Test to return a borrowed book.
        """
        Library.add_book("12345", "Test Book", "Author", 2023)
        Library.borrow_book("12345")
        Library.return_book("12345")
        books = Library.view_available_books()
        self.assertEqual(len(books), 1)  # Book is returned, so it should be available

    def test_borrow_unavailable_book(self):
        """
        Test for borrowing a book that is not available.
        """
        Library.add_book("12345", "Test Book", "Author", 2023)
        Library.borrow_book("12345")
        with self.assertRaises(ValueError):  # Should raise an error for unavailable book
            Library.borrow_book("12345")

    def test_return_unborrowed_book(self):
        """
        Test for returning a book that has not been borrowed.
        """
        Library.add_book("12345", "Test Book", "Author", 2023)
        with self.assertRaises(ValueError):  # Should raise an error for returning unborrowed book
            Library.return_book("12345")


if __name__ == "__main__":
    unittest.main()
