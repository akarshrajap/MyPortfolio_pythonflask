import sqlite3
import os
from flask import Flask, render_template, request, g, redirect, flash, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkeyforflashingmessages') # Required for flash messages
DATABASE = os.environ.get('DATABASE_PATH', 'database.db')

# --- Database Helper Functions ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row # Allows accessing columns by name
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.cursor().execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        db.commit()

# --- Routes ---

# 1. Main Page Route
@app.route('/')
def index():
    # Example data passed from backend to Jinja2 template
    portfolio_data = {
        'name': 'Akarsh Raj A P',
        'title': 'Python Full Stack Developer Trainer',
        'bio': 'Strategic Python Full Stack Developer and Cloud Architect with over 7 years of industry experience. Having transitioned from a Senior Consultant role at LTIMindtree to a dedicated Freelance Trainer, I bridge the gap between complex software engineering and classroom learning. I specialize in AWS/Azure infrastructure, MERN stack development, and Python automation, helping the next generation of developers build scalable, production-ready applications.',
        'year': 2026
    }
    return render_template('index.html', data=portfolio_data)

# 2. Contact Form Submission Route
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Simple validation
        if not name or not email or not message:
            flash('Error: All fields are required!', 'error')
            return redirect(url_for('index', _anchor='contact'))

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
                (name, email, message)
            )
            db.commit()
            flash('Success! Your message has been sent.', 'success')
        except sqlite3.Error as e:
            flash(f'Database Error: {e}', 'error')
        
        # Redirect back to the home page, specifically to the contact section anchor
        return redirect(url_for('index', _anchor='contact'))

# Initialize database at startup so it also works under Gunicorn on Render.
init_db()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 4000)),
        debug=os.environ.get('FLASK_DEBUG', '0') == '1'
    )