"""
Task management routes and logic.
Implements CRUD operations with error handling and validation.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from models import db, Task
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.wrappers import Response


tasks = Blueprint("tasks", __name__)


def validate_task_data(form_data: dict[str]) -> tuple[bool, list[str] | None]:
    """Validate task form data."""
    errors: list[str] | None = []

    # Title
    if not form_data.get("title"):
        errors.append("Title is required.")
    elif len(form_data["title"]) > 200:
        errors.append("Title must be under 200 characters long.")

    # Description
    if not form_data.get("description"):
        errors.append("Description is required.")
    elif len(form_data["description"]) > 1000:
        errors.append("Description must be under 1000 characters long.")

    # Due date
    if form_data.get("due_date"):
        try:
            due_date = datetime.fromisoformat(form_data["due_date"])
            if due_date < datetime.now():
                errors.append("Due date can't be in the past")
        except ValueError:
            errors.append("Invalid date format. Use YYYY-MM-DD HH-MM.")

    # Priorities
    valid_priorities = ["low", "medium", "high"]
    if form_data.get("priority") not in valid_priorities:
        errors.append("Invalid priority level.")

    return len(errors) == 0, errors


@tasks.route("/dashboard")
@login_required
def dashboard():
    """Main task dashboard."""
    # Get all user's tasks
    user_tasks = (
        Task.query.filter_by(user_id=current_user.id)
        .order_by(Task.created_at.desc())
        .all()
    )
    return render_template("dashboard.html", tasks=user_tasks)


@tasks.route("/create-task", methods=["GET", "POST"])
@login_required
def create_task() -> Response:
    """Handles task creation with validation and error handling."""
    if request.method == "POST":
        # Validate
        is_valid, errors = validate_task_data(request.form)
        if not is_valid:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("tasks.create_task"))

        # Create a new task
        new_task = Task(
            title=request.form["title"],
            description=request.form["description"],
            priority=request.form["priority"],
            category=request.form.get("category", "general"),
            due_date=(
                datetime.fromisoformat(request.form["due_date"])
                if request.form.get("due_date")
                else None
            ),
            user_id=current_user.id,
        )

        # Commit to database with rollback
        try:
            db.session.add(new_task)
            db.session.commit()
            flash("Task created successfully!", "success")
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Database error: {e}", "error")

        return redirect(url_for("tasks.dashboard"))
    return render_template("create_task.html")


@tasks.route("/edit-task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id: int) -> Response:
    """Task editing feature."""
    # Task query with simple validation
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        flash("Task not found or unauthorized", "error")
        return redirect(url_for("tasks.dashboard"))

    # Editing the tasks
    if request.method == "POST":
        is_valid, errors = validate_task_data(request.form)
        if not is_valid:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("tasks.edit_task", task_id=task_id))

        # Update Task data
        task.title = request.form["title"]
        task.description = request.form["description"]
        task.priority = request.form["priority"]
        task.category = request.form.get("category", "general")
        task.due_date = (
            datetime.fromisoformat(request.form["due_date"])
            if request.form.get("due_date")
            else None
        )

        # Commit to database with rollback
        try:
            db.session.commit()
            flash("Task updated successfuly!", "success")
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Database error: {e}", "error")

        return redirect(url_for("tasks.dashboard"))

    return render_template("edit_task.html", task=task)


@tasks.route("/complete-task/<int:task_id>", methods=["GET", "POST"])
@login_required
def complete_task(task_id: int) -> Response:
    """Complete tasks."""
    # Task query with simple validation
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        flash("Task not found or unauthorized", "error")
        return redirect(url_for("tasks.dashboard"))

    # Mark complete and commit with rollback
    try:
        if task.completed:
            task.mark_incomplete()
            flash("Task marked as incomplete.", "info")
        else:
            task.mark_complete()
            flash("Task marked as complete.", "info")
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {e}", "error")

    return redirect(url_for("tasks.dashboard"))


@tasks.route("/delete-task/<int:task_id>")
@login_required
def delete_task(task_id: int) -> Response:
    """Delete task."""
    # Task query
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        flash("Task not found or unauthorized", "error")
        return redirect(url_for("tasks.dashboard"))

    # Delete and commit with rollback
    try:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted successfully", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {e}", "error")

    return redirect(url_for("tasks.dashboard"))
