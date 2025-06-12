import pytest
import os
import project
from project import Task


# Fixtures for testing
@pytest.fixture(autouse=True)
def clean_tasks():
    """Clean up tasks list before and after each test."""
    # Store original tasks
    original_tasks = project.tasks.copy()
    project.tasks.clear()

    yield

    # Restore original tasks
    project.tasks.clear()
    project.tasks.extend(original_tasks)


def test_task_creation():
    """Test basic Task object creation."""
    task = Task(1, "Test task", "High")

    assert task.id == 1
    assert task.description == "Test task"
    assert task.priority == "High"
    assert not task.completed
    assert task.created is not None


def test_task_validation():
    """Test Task input validation."""
    # Test empty description
    with pytest.raises(ValueError):
        Task(1, "", "High")

    # Test whitespace-only description
    with pytest.raises(ValueError):
        Task(1, "   ", "High")

    # Test invalid priority
    with pytest.raises(ValueError):
        Task(1, "Test task", "Invalid")


def test_task_mark_complete():
    """Test marking task as complete."""
    task = Task(1, "Test task", "Medium")

    # First completion should succeed
    assert task.mark_complete()
    assert task.completed

    # Second completion should return False (already completed)
    assert not task.mark_complete()


def test_task_to_dict():
    """Test task dictionary conversion."""
    task = Task(1, "Test task", "Low", "2025-01-01", True)
    task_dict = task.to_dict()

    expected = {
        "id": 1,
        "description": "Test task",
        "priority": "Low",
        "created": "2025-01-01",
        "completed": True,
    }
    assert task_dict == expected


def test_task_from_dict():
    """Test creating task from dictionary."""
    task_dict = {
        "id": "2",
        "description": "Test task 2",
        "priority": "High",
        "created": "2025-01-01",
        "completed": True,
    }

    task = Task.from_dict(task_dict)
    assert task.id == 2
    assert task.description == "Test task 2"
    assert task.priority == "High"
    assert task.completed


def test_add_task():
    """Test adding tasks to the list."""
    # Test successful addition
    assert project.add_task("Test task", "High")
    assert len(project.tasks) == 1
    assert project.tasks[0].description == "Test task"
    assert project.tasks[0].priority == "High"

    # Test numeric priority conversion
    assert project.add_task("Test task 2", 2)
    assert len(project.tasks) == 2
    assert project.tasks[1].priority == "Medium"


def test_add_task_validation():
    """Test add_task input validation."""
    # Test empty description
    assert not project.add_task("", "High")
    assert len(project.tasks) == 0

    # Test whitespace-only description
    assert not project.add_task("   ", "High")
    assert len(project.tasks) == 0

    # Test invalid numeric priority
    assert not project.add_task("Test task", 5)
    assert len(project.tasks) == 0


def test_mark_task_complete():
    """Test marking tasks as complete."""
    # Add test tasks
    project.add_task("Task 1", "High")
    project.add_task("Task 2", "Medium")

    # Test successful completion
    assert project.mark_task_complete(1)
    assert project.tasks[0].completed

    # Test completing already completed task
    assert not project.mark_task_complete(1)

    # Test invalid task ID
    assert not project.mark_task_complete(99)


def test_mark_task_complete_empty_list():
    """Test marking task complete when no tasks exist."""
    assert not project.mark_task_complete(1)


def test_delete_task():
    """Test deleting tasks."""
    # Add test tasks
    project.add_task("Task 1", "High")
    project.add_task("Task 2", "Medium")
    project.add_task("Task 3", "Low")

    # Delete middle task
    assert project.delete_task(2)
    assert len(project.tasks) == 2

    # Check ID reindexing
    assert project.tasks[0].id == 1
    assert project.tasks[0].description == "Task 1"
    assert project.tasks[1].id == 2
    assert project.tasks[1].description == "Task 3"

    # Test invalid task ID
    assert not project.delete_task(99)


def test_delete_task_empty_list():
    """Test deleting task when no tasks exist."""
    assert not project.delete_task(1)


def test_save_and_load_tasks():
    """Test saving and loading tasks with actual CSV file."""
    try:
        # Add test tasks
        project.add_task("Task 1", "High")
        project.add_task("Task 2", "Medium")

        # Test save
        assert project.save_tasks()
        assert os.path.exists("tasks.csv")

        # Clear tasks and test load
        project.tasks.clear()
        assert project.load_tasks()
        assert len(project.tasks) == 2
        assert project.tasks[0].description == "Task 1"
        assert not project.tasks[0].completed
        assert project.tasks[1].description == "Task 2"
        assert not project.tasks[1].completed

    finally:
        # Cleanup test file
        if os.path.exists("tasks.csv"):
            os.unlink("tasks.csv")


def test_load_nonexistent_file():
    """Test loading from non-existent file."""
    assert not project.load_tasks()
    assert len(project.tasks) == 0


def test_task_str_method():
    """Test Task string representation."""
    task1 = Task(1, "Test task", "High", completed=False)
    task2 = Task(2, "Completed task", "Low", completed=True)

    assert "○" in str(task1)  # Pending task
    assert "✓" in str(task2)  # Completed task
    assert "Test task" in str(task1)
    assert "High" in str(task1)


def test_security_validation():
    """Test security validation in Task description."""
    # Test XSS attempts
    with pytest.raises(ValueError):
        Task(1, "<script>alert('xss')</script>", "High")
        
    # Test SQL injection attempts
    with pytest.raises(ValueError):
        Task(1, "'; DROP TABLE tasks; --", "High")
        
    # Test valid characters (should pass)
    task1 = Task(1, "Buy groceries: milk, bread!", "High")
    assert task1.description == "Buy groceries: milk, bread!"
    task2 = Task(2, "Meeting at 3:00 PM (Room 303)", "Medium")    
    assert task2.description == "Meeting at 3:00 PM (Room 303)"


def test_task_edge_cases():
    """Test edge cases for description validation."""
    # Test Unicode characters (should fail)
    with pytest.raises(ValueError):
        Task(1, "Café meeting ☕", "High")
        
    # Test very long description (should pass)
    long_desc = "A" * 100
    task = Task(1, long_desc, "High")
    assert task.description == long_desc