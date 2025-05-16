import os
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about-us')
def about_us():
    return render_template('about-us.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/user_info')
def user_info():
    return render_template('user_info.html')

@app.route('/login')
def login():
    return render_template('login.html')

# Registration Submission (check existing or insert new)
@app.route('/submit-registration', methods=['POST'])
def submit_registration():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()

    if user:
        conn.close()
        return render_template('user_info.html', user=user)  # User already exists
    else:
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return redirect('/thankyou')  # New user registered
        except sqlite3.IntegrityError:
            conn.close()
            return "<h3>Username already exists. Try another.</h3>"

# Thank You Page
@app.route('/thankyou')
def thankyou():
    return "<h2>Registration Successful!</h2><a href='/'>Go back</a>"

# Admin Page to view all users
@app.route('/admin')
def admin():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    return render_template('admin.html', users=users)

# 404 Error Handler
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
