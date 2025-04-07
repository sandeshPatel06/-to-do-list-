from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

# Secret key and database URI
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_secret_key')

import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    task_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

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

    # Get the current user
    user = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        task = request.form['task']
        task_time = request.form.get('task-time')
        
        if task_time:
            # Ensure proper datetime format (i.e., datetime-local format)
            task_time = datetime.datetime.strptime(task_time, "%Y-%m-%dT%H:%M")
        else:
            task_time = datetime.datetime.now()

        # Create a new task for the user
        new_task = Task(task=task, task_time=task_time, user_id=user.id)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(user_id=user.id).all()
    return render_template('todo_list.html', tasks=tasks)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
