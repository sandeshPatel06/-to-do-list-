from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask_migrate import Migrate



app = Flask(__name__)

# Secret key and database URI
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_secret_key')

import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Initialize SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Define the Task model
# Define the Task model with a 'completed' field
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=True)  
    task_time = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

    __table_args__ = (
        db.UniqueConstraint('task', 'task_time', 'user_id', name='unique_task_per_user'),
    )

# Create tables in the database (only if they don't exist already)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # if 'username' in session:
        # return redirect(url_for('todo_list'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch the user from the database
        user = User.query.filter_by(username=username).first()

        # Check if user exists and if the password is correct
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('todo_list'))
        else:
            flash("Invalid credentials", "error")
            return render_template('login.html')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose another.", "error")
            return render_template('register.html')

        # Create a new user
        new_user = User(username=username, password=password_hash)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/todo_list', methods=['GET', 'POST'])
def todo_list():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        task = request.form['task']
        description = request.form.get('description')  # Get description
        task_time = request.form.get('task-time')

        if task_time:
            # Convert the task time to a datetime object
            task_time = datetime.strptime(task_time, "%Y-%m-%dT%H:%M")
            
            # Get the current datetime
            current_time = datetime.now()

            # Check if the task time is in the past
            if task_time < current_time:
                flash("You cannot set a task in the past.", "error")
                return redirect(url_for('todo_list'))

        else:
            task_time = datetime.now()

        # Check if the task already exists for the user at the same time
        existing_task = Task.query.filter_by(task=task, task_time=task_time, user_id=user.id).first()

        if existing_task:
            flash("Task already exists!", "info")
        else:
            try:
                # Add the new task if it doesn't exist
                new_task = Task(task=task, description=description, task_time=task_time, user_id=user.id)
                db.session.add(new_task)
                db.session.commit()
                flash("Task added successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash("There was an error adding the task.", "error")

        # Redirect to the GET route after POST (to avoid resubmission on refresh)
        return redirect(url_for('todo_list'))

    tasks = Task.query.filter_by(user_id=user.id).all()
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M")  # Get current time for client-side validation
    return render_template('todo_list.html', tasks=tasks, username=user.username, current_time=current_time)


@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['username']).first()

    # Fetch the task to be edited
    task = Task.query.filter_by(id=task_id, user_id=user.id).first()

    if not task:
        flash("Task not found or you don't have permission to edit this task.", "error")
        return redirect(url_for('todo_list'))

    if request.method == 'POST':
        task.task = request.form['task']
        task.description = request.form.get('description')  # Update description
        task_time = request.form.get('task-time')
        
        if task_time:
            task_time = datetime.strptime(task_time, "%Y-%m-%dT%H:%M")
            
            # Get the current datetime
            current_time = datetime.now()

            # Check if the task time is in the past
            if task_time < current_time:
                flash("You cannot set a task in the past.", "error")
                return redirect(url_for('edit_task', task_id=task.id))

            task.task_time = task_time

        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect(url_for('todo_list'))

    # Set the current time for client-side validation
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M")
    return render_template('edit_task.html', task=task, current_time=current_time)


@app.route('/delete_task/<int:task_id>', methods=['GET'])
def delete_task(task_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    # Get the current user
    user = User.query.filter_by(username=session['username']).first()

    # Find the task by id and make sure it's the current user's task
    task_to_delete = Task.query.filter_by(id=task_id, user_id=user.id).first()

    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash("Task deleted successfully.", "success")
    else:
        flash("Task not found or you don't have permission to delete this task.", "error")

    return redirect(url_for('todo_list'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/toggle_complete/<int:task_id>', methods=['GET'])
def toggle_complete(task_id):
    if 'username' not in session:
        flash("You need to log in first.", "error")
        return redirect(url_for('login'))

    # Get the current user based on the username from the session
    user = User.query.filter_by(username=session['username']).first()

    if not user:
        flash("User not found. Please log in again.", "error")
        return redirect(url_for('login'))

    # Find the task by id and make sure it's the current user's task
    task = Task.query.filter_by(id=task_id, user_id=user.id).first()

    if task:
        # Toggle the 'completed' field
        task.completed = not task.completed
        db.session.commit()
        flash("Task status updated.", "success")
    else:
        flash("Task not found or you don't have permission to modify this task.", "error")

    return redirect(url_for('todo_list'))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
