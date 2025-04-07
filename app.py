from flask import Flask, render_template, request, redirect, url_for, session
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Hardcoded users for demonstration
users = {"user1": "password1", "user2": "password2"}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('todo_list'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if users.get(username) == password:
            session['username'] = username
            return redirect(url_for('todo_list'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/todo_list', methods=['GET', 'POST'])
def todo_list():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        task = request.form['task']
        task_time = request.form.get('task-time')  # Using get() to avoid missing key error
        if task_time:
            task_time = datetime.datetime.strptime(task_time, "%Y-%m-%dT%H:%M")
        else:
            task_time = datetime.datetime.now()  # Default to current time if not provided
        
        # Ensure tasks are stored correctly in session
        if 'tasks' not in session:
            session['tasks'] = []

        # Store task and time in session
        session['tasks'].append((task, task_time.strftime("%Y-%m-%dT%H:%M")))

    tasks = session.get('tasks', [])
    print("Tasks:", tasks)  # This will print tasks to the console
    return render_template('todo_list.html', tasks=tasks)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
