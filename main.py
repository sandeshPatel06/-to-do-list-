from waitress import serve
from app import app  # Assuming your Flask app is named `app` in `app.py`

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)
