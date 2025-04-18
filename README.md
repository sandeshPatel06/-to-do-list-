# Flask To-Do App

A simple To-Do app built with Flask, SQLAlchemy, and SQLite. This app allows users to register, log in, create tasks, and view them in a list format. Each task is associated with a user, and tasks are stored in an SQLite database.

## Features

- User authentication (Login/Registration)
- Task creation with an optional due date/time
- Display tasks for each user
- Logout functionality


## Installation

1. **Clone the repository** to your local machine:

   ```bash
   git clone https://github.com/sandeshPatel06/-to-do-list-.git
   cd -to-do-list-
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On Mac/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the database**:

   The app uses SQLite, and the database will be created automatically when the application starts. If it's not created, you can manually run the following:

   ```python
   from app import db
   with app.app_context():
       db.create_all()
   ```

## Usage

1. **Run the application**:

   ```bash
   python app.py
   ```

2. Open your browser and go to [http://localhost:5000](http://localhost:5000) to start using the app.

### Available Routes

- `/` - Home page
- `/login` - Login page for registered users
- `/register` - Registration page to create a new user
- `/todo_list` - Page to manage tasks (only accessible if logged in)
- `/logout` - Log out the current user and redirect to the login page

### Example Workflow

1. **Register**: Create an account using the `/register` page.
2. **Login**: Use the `/login` page to log in.
3. **Add Tasks**: On the `/todo_list` page, you can add tasks and view them.
4. **Logout**: Use the `/logout` route to log out of the app.

## File Structure

```
/app.py               # Main application file (Flask app)
/templates/            # Folder containing HTML templates
    /index.html        # Home page template
    /login.html        # Login page template
    /register.html     # Register page template
    /todo_list.html    # To-Do list page template
/static/               # Static files (e.g., CSS, JavaScript)
    /styles.css        # CSS file for styling the app
/requirements.txt      # List of dependencies (Flask, SQLAlchemy, etc.)
```

## Dependencies

- Flask
- Flask-SQLAlchemy
- Werkzeug (for password hashing)

## License

---

Feel free to contribute to this project or create a fork. Open issues or pull requests for any feature requests or bug fixes are welcome!
```

### Key Markdown Elements:
- **Headings**: Used `#` to create headers and sub-headers (e.g., `## Features`, `## Installation`, etc.).
- **Code Blocks**: Enclosed in triple backticks (```) for commands and code snippets, such as installing dependencies and running the app.
- **Links**: `[Link Text](URL)` format used for the license file and GitHub repository URL.
- **Lists**: Both ordered (numbered) and unordered (bulleted) lists are used for features, instructions, and file structure.
- **Code Formatting**: Inline code is wrapped in single backticks (e.g., `python app.py`).

Make sure to update the repository link in the `git clone` command to match your actual repository's URL. If you have a `requirements.txt` file, it should be included in your repository.

