"""
Database models:
This file defines the database schema and relationship between different entities.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column, relationship

# SQLAlchemy init
db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for storing user account data."""

    __tablename__ = "users"

    # Primary key
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)

    # User credentials
    username: Mapped[str] = mapped_column(
        db.String(80), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        db.String(120), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(db.String(255), nullable=False)

    # User profile info
    first_name: Mapped[str] = mapped_column(db.String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(db.String(50), nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )

    # Relationship to tasks - one users with many tasks
    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def set_password(self, password: str) -> None:
        """Hash and store the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify a password with stored hash."""
        return check_password_hash(self.password_hash, password)

    def get_full_name(self) -> str:
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """User object representation for debugging."""
        return f"<User({self.username}, {self.email})>"


class Task(db.Model):
    """
    Task model for storing tasks and their properties.
    Each task belongs to a specific user and tracks completion status.
    """

    __tablename__ = "tasks"

    # Primary key
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)

    # Task content
    title: Mapped[str] = mapped_column(db.String(200), nullable=False)
    description: Mapped[str] = mapped_column(db.Text, nullable=False)

    # Status (true, false) and priority (low, medium, high)
    completed: Mapped[bool] = mapped_column(db.Boolean, default=False, nullable=False)
    priority: Mapped[str] = mapped_column(
        db.String(20), default="medium", nullable=False
    )

    # Category
    category: Mapped[str] = mapped_column(
        db.String(50), default="general", nullable=False
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )
    due_date: Mapped[datetime | None] = mapped_column(db.DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(db.DateTime, nullable=True)

    # Foreign key linking task to user
    user_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="tasks")

    def mark_complete(self) -> None:
        """Mark the task completed and record completion time."""
        self.completed = True
        self.completed_at = datetime.now()

    def mark_incomplete(self) -> None:
        """Mark incompleted and clear record time."""
        self.completed = False
        self.completed_at = None

    def check_overdue(self) -> bool:
        """Check if the task is past due date and not completed."""
        if self.due_date and not self.completed:
            return datetime.now() > self.due_date
        return False

    def get_priority_cls(self) -> str:
        """Return class name based on priority for CSS styling."""
        priority_cls = {
            "low": "priority-low",
            "medium": "priority-medium",
            "high": "priority-high",
        }
        return priority_cls.get(self.priority)

    def __repr__(self) -> str:
        """Task object representation for debugging."""
        return f"<Task({self.id}, {self.title}, {self.priority})>"
