# Flask_app_tests
*Andrej Banas*

## Overview
This is the backend part of a simple item management application built with Python and Flask. It provides RESTful APIs to create, view, update, and delete items, along with a form for submitting item details. It’s a lightweight app designed to show how Flask can handle basic tasks like saving data and responding with JSON.

## Technologies Used

### Frameworks and Libraries
- **Flask** (Core framework for routes and API)
- **Flask-SQLAlchemy** (Database handling)
- **Flask-WTF** (Form creation and validation)
- **pytest** (pytest, pytest-flask, pytest-cov for testing)

### Database Technologies
- **SQLite** (Simple database with in-memory testing and file-based production modes)
- **SQLAlchemy** (Python ORM to work with the database)

### Additional Python Concepts and Skills
- **Functions and Helpers** (Simple utilities like `add_numbers` and `get_home_message`)
- **Forms and Validation** (Using Flask-WTF with `ItemForm`)
- **RESTful APIs** (JSON responses for all endpoints)
- **Testing** (Unit and integration tests with pytest)

### Unit Testing and Integration Testing
- **Unit Testing** (pytest for small functions and routes)
- **Integration Testing** (pytest-flask for database and API tests)

### Security
- **Basic Secret Key** (Used for form security in Flask-WTF)

## Application Features
- **Item Management**
  - Create items with a form or API at `/items` (POST)
  - View all items at `/items` (GET) or one item at `/items/<id>` (GET)
  - Update items at `/items/<id>` (PUT)
  - Delete items at `/items/<id>` (DELETE)
  - Item data stored in SQLite
- **Form Submission**
  - Submit item details at `/submit` with validation (name and description)
- **Simple Calculator**
  - Add two numbers at `/add/<a>/<b>` (e.g., `/add/2/3`)
- **Configuration Modes**
  - Testing mode (in-memory database, debug on)
  - Production mode (file-based `app.db`, debug off)
- **Error Handling**
  - Returns clear error messages for bad inputs (400), missing items (404), or server errors (500)

## Installation and Running the Project
To run this project on your computer, follow these steps:

1. **Clone the Repository**:
   - Use Git in your terminal:
     ```bash
     git clone https://github.com/andrej1991banas/Flask_app_pytests.git
     cd Flask_app_tests

2. **Set Up SQLite Database (for production mode):**
   - You don’t need to install SQLite—it’s built into Python!
   - Run this to create app.db:
     ```bash
      python -c "from app import create_app, db; app = create_app('production'); with app.app_context(): db.create_all()"
     ```

3. **Set Up Python Environment:**
   - Make a virtual environment:
     ``` bash
     python -m venv venv
        ```
4. **Install Required Tools:**
   - Use the requirements.txt file:
      ```bash
       pip install -r requirements.txt
      ```
5. **Run the Application:**
   - Start the app:
     ``` bash
      python app.py
     ```
  - Open your browser at http://127.0.0.1:5000/ to see the welcome message.

6. **Access the Application:**
   - Use a browser or tools like Postman or curl to try the APIs (see examples below).

**Unit Testing**

Tests are in the tests/ folder, with 22 tests covering 98% of the code.
  - Run Tests:
``` bash pytest tests/ ```
  - Check Coverage:
```bash pytest --cov=app --cov-report=term-missing tests/ ```

## Contributions

This project is a showcase of my Python and Flask skills. It’s public so you can see what I’ve done, but please don’t send pull requests or change it. I want to keep it as my example work. Thanks for understanding!









