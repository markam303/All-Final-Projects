"""
Authentication routes and logic:
Handles user registration, login, logout, and session management.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from werkzeug.wrappers import Response
import re


# Create authentication blueprint
auth = Blueprint("auth", __name__)


def validate_email(email: str) -> bool:
    """Validate email format with regex."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,24}$"
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength."""
    if len(password) < 6:
        return False, "Password must contain at least 6 characters."

    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter."

    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."

    return True, "Password is strong enough."


@auth.route("/register", methods=["GET", "POST"])
def register() -> Response:
    """Handles user registration."""
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for("tasks.dashboard"))

    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        # Get form data
        username: str = request.form.get("username", "").strip()
        email: str = request.form.get("email", "").strip().lower()
        first_name: str = request.form.get("first_name", "").strip()
        last_name: str = request.form.get("last_name", "").strip()
        password: str = request.form.get("password", "")

        # Validation
        errors: list[str] = []

        if not username:
            errors.append("Username is required.")
        elif len(username) < 3:
            errors.append("Username must be at least 3 characters long.")
        elif not re.match(r"^[a-zA-Z0-9_]+$", username):
            errors.append("Username can only contain letters, numbers and underscores.")

        if not email:
            errors.append("Email is required.")
        elif not validate_email(email):
            errors.append("Please enter a valid email address.")

        if not first_name:
            errors.append("First name required.")
        if not last_name:
            errors.append("Last name is required.")

        if not password:
            errors.append("Password is required.")
        else:
            is_valid, password_error = validate_password(password)
            if not is_valid:
                errors.append(password_error)

        # Check for dupes
        if User.query.filter_by(username=username).first():
            errors.append("Username already exists.")
        if User.query.filter_by(email=email).first():
            errors.append("Email address already registered.")

        # Print errors if occured
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("register.html")

        # Try to register a new user with commit and rollback
        try:
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            login_user(user, remember=True)
            flash("Registration successful! Welcome to TaskFlow!", "success")
            return redirect(url_for("tasks.dashboard"))

        except Exception as e:
            db.session.rollback()
            flash("An error occured during registration. Please try again.", "error")
            print(f"Registration error: {e}")

        return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login() -> Response:
    """Handles user login."""
    if current_user.is_authenticated:
        return redirect(url_for("tasks.dashboard"))

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username_or_email: str = request.form.get("username_or_email", "").strip()
        password: str = request.form.get("password", "")
        remember_me: bool = bool(request.form.get("remember_me", False))

        if not username_or_email:
            flash("Please enter your username or email.", "error")
            return render_template("login.html")

        # Find user
        if "@" in username_or_email:
            user = User.query.filter_by(email=username_or_email.lower()).first()
        else:
            user = User.query.filter_by(username=username_or_email).first()

        # Check if user exists and password is correct
        if user and user.check_password(password):
            # Login successful
            login_user(user, remember=bool(remember_me))
            flash(f"Welcome back, {user.first_name}!", "success")
            return redirect(url_for("tasks.dashboard"))
        else:
            # Login failed
            flash("Invalid username/email and/or password", "error")

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout() -> Response:
    """Logout, clear session, and redirect to homepage."""
    user_name: str = current_user.first_name
    logout_user()
    flash(f"Goodbye, {user_name}! You've been logged out.", "info")
    return redirect(url_for("auth.login"))
