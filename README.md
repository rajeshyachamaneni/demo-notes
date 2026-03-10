# Flask Firestore Notes Application

This is a simple Flask application that allows you to create, read, update, and delete notes using Google Cloud Firestore as the backend database.

## Features

- Create new notes with a title and content.
- View a list of all notes.
- Edit existing notes.
- Delete notes.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.9+
- pip (Python package installer)
- Docker (if you plan to run the application using Docker)
- Google Cloud Project with Firestore enabled.
- A Firebase service account key JSON file.

## 1. Firebase Setup

1.  Go to your Firebase project in the Google Cloud Console.
2.  Navigate to "Project settings" -> "Service accounts".
3.  Click "Generate new private key" to download a JSON file. Rename this file (e.g., `serviceAccountKey.json`) and place it in the root directory of this project (`demo-notes/`).
4.  **Important**: Update the `app.py` file with the correct path to your service account key file:
    ```python
    cred = credentials.Certificate('path/to/your/serviceAccountKey.json') # Change this line
    ```
    Replace `'path/to/your/serviceAccountKey.json'` with `'serviceAccountKey.json'` or the actual path if you placed it elsewhere.

## 2. Local Setup and Run

1.  **Navigate to the project directory:**
    ```bash
    cd demo-notes
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Flask application:**
    ```bash
    export FLASK_APP=app.py
    flask run --host=0.0.0.0
    ```
    The application will be accessible at `http://127.0.0.1:5000` or `http://localhost:5000`.

## 3. Docker Setup and Run

1.  **Navigate to the project directory:**
    ```bash
    cd demo-notes
    ```

2.  **Build the Docker image:**
    ```bash
    docker build -t flask-notes-app .
    ```

3.  **Run the Docker container:**
    Make sure your `serviceAccountKey.json` is in the `demo-notes` directory or adjust the `COPY` command in the `Dockerfile` to include its path.
    ```bash
    docker run -p 5000:5000 flask-notes-app
    ```
    The application will be accessible at `http://localhost:5000`.

## Important Security Note:

For production environments, storing your `serviceAccountKey.json` directly in the project directory or Docker image is not recommended. Consider using environment variables, Google Cloud Secret Manager, or other secure methods to inject credentials into your application.
# demo-notes
