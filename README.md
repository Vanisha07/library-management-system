# Library Management System

A simple Library Management System to add, manage, borrow and return books, and validate book details using Python and SQLite.

## Features:
- Add books to the library
- Borrow books
- Return books
- View available books
- Validate book details (ISBN, title, author, and year)

## Prerequisites
- Python 3.x
- SQLite (comes pre-installed with Python)

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system
   ```

2. **Install Dependencies**
   Although SQLite is built into Python, you may need to install some additional packages if you use them (e.g., `unittest` is built-in, no need to install it).
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Program**
   - To run the Library Management System, execute the following Python script:
   ```bash
   python library_management_system.py
   ```

4. **Run Tests**
   - To run the tests, use the `unittest` framework:
   ```bash
   python -m unittest test_library_management_system.py
   ```

## Test Results
Test cases can be executed using the following:
```bash
python -m unittest test_library_management_system.py
