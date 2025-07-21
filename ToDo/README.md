# Todo List Application

#### Video Demo: https://youtu.be/BbtfzUMcw8A

## Description
A command-line Todo List application built with Python that demonstrates advanced programming concepts including object-oriented design, security validation, and comprehensive testing. This project showcases proper software engineering practices with clean architecture, input sanitization, and robust error handling.

The application allows users to manage their daily tasks through an intuitive command-line interface, with automatic data persistence using CSV files. Each task includes a description, priority level, creation date, and completion status.


## Features
- Add tasks with priority levels (High/Medium/Low)
- View tasks in formatted table
- Mark tasks as complete
- Delete tasks
- Automatic data persistence to CSV


## Files

| File               | Purpose          | Description                                   |
|--------------------|------------------|-----------------------------------------------|
| `project.py`       | Main Application | Contains Task class and all application logic |
| `test_project.py`  | Test Suite       | Comprehensive pytest-based testing            |
| `tasks.csv`        | Data Storage     | Auto-generated CSV file for task persistence  |
| `requirements.txt` | Dependencies     | External library requirements                 |
| `README.md`        | Documentation    | Project documentation and usage guide         |



## Getting Started
0. Ensure you have Python 3.7 or newer
1. Install dependencies: `pip install -r requirements.txt`
2. Run application: `python project.py`
3. Follow on-screen instructions


## Design Choices
1. **Task Class**: Encapsulates task properties and methods
2. **Standalone Functions**: Handle task list management
3. **CSV Storage**: Simple persistent storage solution
4. **Input Validation**: Comprehensive error checking

	### Core Functionality
	- **Add Tasks**: Create new tasks with descriptions and priority levels (High/Medium/Low)
	- **View Tasks**: Display all tasks in a beautifully formatted table using tabulate
	- **Mark Complete**: Toggle task completion status with validation
	- **Delete Tasks**: Remove tasks with automatic ID reindexing
	- **Data Persistence**: Automatic saving/loading to CSV file between sessions

	### Security Features
	- **Input Validation**: Regex-based sanitization preventing malicious content
	- **XSS Protection**: Blocks script tags and dangerous HTML elements
	- **SQL Injection Prevention**: Filters common injection patterns
	- **Safe Character Set**: Allows only letters, numbers, spaces, and common punctuation

	### User Experience
	- **ASCII Art Welcome**: Custom TODO banner for visual appeal
	- **Error Handling**: Comprehensive validation with user-friendly messages
	- **Input Recovery**: Elegant handling of invalid inputs with retry prompts
	- **Progress Tracking**: Shows loaded task count and completion status


## Technical Architecture

### Object-Oriented Design
- **class Task**:
	- Properties: id, description, priority, created, completed
	- Methods: mark_complete(), to_dict(), from_dict()
	- Security: Built-in description validation with regex

### Functional Components
- **Task Management**: add_task(), delete_task(), mark_task_complete()
- **Data Operations**: save_tasks(), load_tasks() with error handling
- **User Interface**: view_tasks(), print_todo_ascii(), main()


## Testing

**To run the test suite**:
pytest test_project.py

### Test Coverage
- **Task Creation & Validation**: Basic object instantiation and input validation
- **CRUD Operations**: Add, view, update, delete functionality
- **File I/O**: Save/load operations with error handling
- **Security**: Malicious input detection and prevention
- **Edge Cases**: Empty lists, invalid IDs, corrupted data


## Challenges
1. **OOP/Functional Balance**: Maintaining clean separation
2. **File I/O Safety**: Atomic writes and error handling
3. **Task ID Management**: Reindexing after deletions
4. **Test Isolation**: Preventing tests from interfering with each other

## Future Improvements
1. Add user authentication
2. Implement due dates
3. Add search/filter functionality
4. Create GUI interface
5. Add editing features
6. Export to PDF


## License

This project is for educational purposes as part of Harvard CS50P's Final Project submission.
