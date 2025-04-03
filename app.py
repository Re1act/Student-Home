from flask import Flask, render_template, redirect, request, session, url_for
from flask_session import Session
from datetime import timedelta, datetime, time
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

# Initialize Flask app
app = Flask(__name__)

app.secret_key = "xry89fxb"
app.permanent_session_lifetime = timedelta(days=2)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database and session
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Session(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

# Define Schedule model
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(30), nullable=False)
    time = db.Column(db.Time, nullable=False)

    def __init__(self, user_id, class_name, location, time):
        self.user_id = user_id
        self.class_name = class_name
        self.location = location
        self.time = time

# Define Assignment model
class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Not Started")

    def __init__(self, user_id, title, due_date, status="Not Started"):
        self.user_id = user_id
        self.title = title
        self.due_date = due_date
        self.status = status

# Check authentication before each request
@app.before_request
def check_authentication():
    if "user_id" in session and request.endpoint == "register":
        return redirect(url_for("index"))
    elif "user_id" not in session and request.endpoint not in ["login", "register", "static"]:
        return redirect(url_for("register"))

# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return "Error: Username and password required"

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return "Error: Username already taken"

    user = User(username, password)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return f"Error: {str(error)}"

    return redirect(url_for("login"))

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Error: Username and password required"

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        session.permanent = True
        session["user_id"] = user.id
        return redirect(url_for("index"))
    else:
        return "Error: Invalid username or password"

# Logout route
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/register")

# Index route
@app.route("/", methods=["GET", "POST"])
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    assignments = Assignment.query.filter_by(user_id=session["user_id"]).all()
    return render_template("index.html", assignments=assignments)

# GPA route
@app.route("/gpa", methods=["GET", "POST"])
def gpa():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "GET":
        return render_template("gpa.html")

# Assignment route
@app.route("/assignment", methods=["GET", "POST"])
def assignment():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form.get("assignment_title")
        due_date = request.form.get("assignment_date")
        status = request.form.get("status")
        if not title or not due_date:
            return "Error: all fields required"
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            return "Error: Invalid date format"
        user_id = session["user_id"]
        new_assignment = Assignment(
            user_id=user_id,
            title=title,
            due_date=due_date,
            status=status
        )
        try:
            db.session.add(new_assignment)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return f"Error: {str(error)}"
        return redirect(url_for("assignment"))
    else:
        assignments = Assignment.query.filter_by(user_id=session["user_id"]).all()
        return render_template("assignment.html", assignments=assignments)

# Delete assignment route
@app.route("/delete_assignment/<int:id>", methods=["GET", "POST"])
def delete_assignment(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    assignment = Assignment.query.get(id)
    if assignment and assignment.user_id == session["user_id"]:
        try:
            db.session.delete(assignment)
            db.session.commit()
            return redirect(url_for("assignment"))
        except Exception as error:
            db.session.rollback()
            return f"Error: {str(error)}"
    else:
        return "Error: Assignment not found"

# Edit assignment route
@app.route("/edit_assignment/<int:id>", methods=["GET", "POST"])
def edit_assignment(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    assignment = Assignment.query.get(id)

    if not assignment or assignment.user_id != session["user_id"]:
        return "Error: Assignment not found"

    if request.method == "POST":
        title = request.form.get("assignment_title")
        due_date = request.form.get("assignment_date")
        status = request.form.get("status")

        if not title or not due_date or not status:
            return "Error: All fields are required"

        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            return "Error: Invalid date format"

        assignment.title = title
        assignment.due_date = due_date
        assignment.status = status

        try:
            db.session.commit()
            return redirect(url_for("assignment"))
        except Exception as error:
            db.session.rollback()
            return f"Error: {str(error)}"

    return render_template("edit_assignment.html", assignment=assignment)

# Schedule route
@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_schedule = Schedule.query.filter_by(user_id=session["user_id"]).all()
    return render_template("schedule.html", schedule=user_schedule)

@app.route("/init_db", methods=["GET"])
def init_db():
    try:
        with app.app_context():  # Ensure app context is active
            db.create_all()
        return "Database initialized successfully!"
    except Exception as e:
        return f"Error initializing database: {str(e)}"

# Edit schedule route
@app.route("/edit_schedule", methods=["GET", "POST"])
def edit_schedule():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("edit_schedule.html")

    num_classes = request.form.get("numClasses")
    if not num_classes or not num_classes.isdigit():
        return "Invalid number of classes"

    num_classes = int(num_classes)
    try:
        Schedule.query.filter_by(user_id=session["user_id"]).delete()
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return f"Error: {str(error)}"

    for i in range(num_classes):
        class_name = request.form.get(f"class{i}")
        class_location = request.form.get(f"classLocation{i}")
        class_time = request.form.get(f"time{i}")

        if not class_name or not class_location or not class_time:
            return f"Missing data for class {i}"

        try:
            class_time = datetime.strptime(class_time, "%H:%M").time()
            new_row = Schedule(
                user_id=session["user_id"],
                class_name=class_name,
                location=class_location,
                time=class_time
            )
            db.session.add(new_row)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return f"Error: {str(error)}"

    return redirect(url_for("schedule"))
