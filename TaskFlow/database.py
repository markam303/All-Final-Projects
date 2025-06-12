"""
Database initialization and configuration:
Handles setup, creation, initial data seed.
"""

from flask import Flask
from models import db, User, Task
from datetime import datetime, timedelta


def init_database(app: Flask) -> None:
    """Initialize the database with the Flask app."""
    # Create all tables
    with app.app_context():
        db.create_all()
        # Check if need to create demo data
        if User.query.count() == 0:
            create_demo_data()


def create_demo_data() -> None:
    """Create sample data for demonstration."""
    demo_user = User(
        username="demo_user",
        email="demo@taskflow.com",
        first_name="Demo",
        last_name="User",
    )
    demo_user.set_password("demo123")

    db.session.add(demo_user)
    db.session.flush()

    # List of dicts showcasing different features
    sample_tasks = [
        {
            "title": "Complete CS50 Final Project",
            "description": "Build a comprehensive web app showcasing full-stack development skills",
            "priority": "high",
            "category": "education",
            "due_date": datetime.now() + timedelta(days=7),
        },
        {
            "title": "Review Flask Documentation",
            "description": "Study Flask best practices and advanced features for web development",
            "priority": "medium",
            "category": "learning",
        },
        {
            "title": "Practice SQL Queries",
            "description": "Work through database exercises to improve query skills",
            "priority": "medium",
            "category": "learning",
            "completed": True,
            "due_date": datetime.now() - timedelta(days=1),
        },
        {
            "title": "Set up development environment",
            "description": "Configure local dev tools and IDE settings",
            "priority": "low",
            "category": "setup",
            "completed": True,
            "due_date": datetime.now() - timedelta(days=3),
        },
    ]

    try:
        for task_data in sample_tasks:
            task = Task(
                title=task_data["title"],
                description=task_data["description"],
                priority=task_data["priority"],
                category=task_data["category"],
                user_id=demo_user.id,
                due_date=task_data.get("due_date"),
                completed=task_data.get("completed", False),
            )

            db.session.add(task)

        # Commit all changes to the db
        db.session.commit()
        print("Demo data created successfully!")

    except Exception as e:
        # If anything goes wrong, rollback the transaction
        db.session.rollback()
        print(f"Error creating demo data: {e}")

