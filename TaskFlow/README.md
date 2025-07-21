# TaskFlow: A Simple and Secure Task Manager

#### Video Demo: https://youtu.be/7xBQnH_hTO0

### What is TaskFlow?

TaskFlow is a web application I built to help people manage their to-do lists in a more organized and effective way. The main goal was to solve a common, real-world problem: keeping track of daily tasks without feeling overwhelmed. While simple checklists are useful, they often lack features for prioritization, categorization, and secure, private access. TaskFlow addresses this by providing a clean, secure, and user-friendly tool that allows individuals to create a personal account and manage their tasks from a central dashboard.

This project was built for my CS50 final project and serves as a practical application of the many concepts I learned throughout the course. It combines a Python and Flask backend for application logic, a SQL database for data persistence, and HTML/CSS with the Jinja templating engine for a dynamic front end. It represents a complete, full-stack application built from scratch.

### Key Features

-   **Secure User Accounts**: The application features a complete user authentication system. You can register for a new account with an email and a strong password, and the system provides clear validation feedback. All passwords are securely **hashed**, which is a critical security practice. The login system is flexible, allowing you to sign in with either your username or email address.
-   **Full Task Management (CRUD)**: You have complete control over your tasks through full CRUD (Create, Read, Update, Delete) functionality. You can create new tasks, view them on your dashboard, edit their details at any time, and delete them once they are no longer needed.
-   **Task Prioritization**: To help you focus on what matters most, you can assign each task a priority level of "low," "medium," or "high." These priorities are represented by different colors on the dashboard, making it easy to see at a glance which tasks require your immediate attention.
-   **Completion and Due Date Tracking**: You can mark tasks as complete, and the application will record the completion timestamp. You can also assign an optional due date to any task, and the dashboard will automatically highlight any tasks that are overdue.
-   **Robust Data Validation**: To prevent errors and enhance security, the application carefully validates all user-submitted data on the server. This includes checking email formats, enforcing password strength, and ensuring that task titles and descriptions are not empty.

### How to Run This Project

Since this is a Flask application, the standard way to run it is with the `flask` command.

1.  **Install the required Python packages**
    ```
    pip install -r requirements.txt
    ```

2.  **Run the app**
    Start the development server:
    ```
    flask run
    ```

4.  **Open the app in your browser**
    Navigate to `http://127.0.0.1:5000`

**Note:** The `if __name__ == "__main__":` block in `app.py` also allows you to run the app with `python app.py`, but using `flask run` is the recommended method for development.

#### Demo Account

When you run the app for the first time, it will automatically create a database and a demo account for you to test with:
-   **Username**: `demo_user`
-   **Password**: `demo123`

### How The Project is Organized
```
taskflow/
├── app.py
├── models.py
├── auth.py
├── tasks.py
├── database.py
├── templates/
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ ├── create_task.html
│ └── edit_task.html
└── taskflow.db
```

I structured the code to be clean, modular, and easy to understand.

-   `app.py`: The main file. It uses an "application factory" pattern to create the Flask app, which makes the project more organized and easier to test.
-   `auth.py`: This file handles everything related to user accounts: registration, login, and logout. I used a **Flask Blueprint** to group all these related functions together.
-   `tasks.py`: This is another Blueprint that contains all the code for creating, viewing, editing, and deleting tasks.
-   `models.py`: This file defines the structure of the database using **SQLAlchemy**. It has two main tables: one for `User`s and one for `Task`s, and it defines the one-to-many relationship between them.
-   `database.py`: A helper file that sets up the database and creates the demo user and tasks when the app is first run.
-   `templates/`: This folder contains all the HTML files that make up the website's pages.

### Design Choices & What I Learned

This project was a fantastic opportunity to apply and deepen my understanding of several important CS50 concepts.

-   **Code Organization with Blueprints**: Instead of writing all the application logic in one enormous file, I used **Flask Blueprints** to separate the code into logical modules (`auth.py` for users, `tasks.py` for tasks). This makes the code much easier to read, debug, and expand in the future.

-   **Database Management with an ORM**: I chose to use **SQLAlchemy**, an Object-Relational Mapper (ORM), to communicate with the database. This was a key decision. Instead of writing raw SQL queries, which can be prone to errors and security risks, the ORM lets me work with Python objects. This approach is safer because SQLAlchemy automatically handles sanitizing inputs, which is the best defense against **SQL injection attacks**. It also made it simple to define the relationship between a user and their tasks, including setting up a `cascade` rule so that when a user's account is deleted, all their tasks are automatically deleted too.

-   **Focus on Security**: Security was a primary consideration.
    1.  **Password Hashing**: Passwords are never, ever stored in plain text. The `set_password` function in the `User` model uses a strong hashing algorithm to protect user credentials.
    2.  **Authorization**: It's not enough to just check if a user is logged in. The application also enforces authorization. Every time a user tries to edit or delete a task, the code first checks that the task actually belongs to them. This crucial step prevents a user from accessing or modifying another user's private data simply by guessing the URL.

-   **Robust Error Handling**: Real-world applications need to handle failures gracefully. I wrapped all database operations (like adding or deleting a task) in `try/except` blocks. If an error occurs during a transaction, `db.session.rollback()` is called. This immediately cancels the operation, preventing the database from being left in a partially updated, corrupted state. The user is then shown a friendly error message via Flask's `flash` system, ensuring a smooth experience even when things go wrong.

---
*This project was created for the CS50: Introduction to Computer Science final project.*
