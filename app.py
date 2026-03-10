import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request, redirect, url_for

# Initialize Flask app
app = Flask(__name__)

# --- Firebase Configuration ---
# IMPORTANT: Replace 'path/to/your/serviceAccountKey.json' with the actual path to your Firebase service account key file.
# This file contains your project's credentials. For production, consider more secure ways to handle credentials.
try:
    cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print(f"Error initializing Firebase: {e}")
    print("Please ensure 'path/to/your/serviceAccountKey.json' is correct and the file exists.")
    db = None # Set db to None if initialization fails to prevent further errors

# --- Routes ---

@app.route('/')
def index():
    notes = []
    if db:
        try:
            notes_ref = db.collection('notes').order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
            for doc in notes_ref:
                note = doc.to_dict()
                note['id'] = doc.id
                notes.append(note)
        except Exception as e:
            print(f"Error fetching notes from Firestore: {e}")
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if db:
            try:
                db.collection('notes').add({
                    'title': title,
                    'content': content,
                    'timestamp': firestore.SERVER_TIMESTAMP
                })
            except Exception as e:
                print(f"Error adding note to Firestore: {e}")
        return redirect(url_for('index'))
    return render_template('create_edit_note.html', note=None)

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_note(id):
    note = None
    if db:
        try:
            note_ref = db.collection('notes').document(id)
            note_doc = note_ref.get()
            if note_doc.exists:
                note = note_doc.to_dict()
                note['id'] = note_doc.id
        except Exception as e:
            print(f"Error fetching note {id} from Firestore: {e}")

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if db and note:
            try:
                db.collection('notes').document(id).update({
                    'title': title,
                    'content': content,
                    'timestamp': firestore.SERVER_TIMESTAMP
                })
            except Exception as e:
                print(f"Error updating note {id} in Firestore: {e}")
        return redirect(url_for('index'))
    return render_template('create_edit_note.html', note=note)

@app.route('/delete/<id>')
def delete_note(id):
    if db:
        try:
            db.collection('notes').document(id).delete()
        except Exception as e:
            print(f"Error deleting note {id} from Firestore: {e}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
