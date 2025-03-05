from flask import Flask, request, render_template_string, session
import sqlite3
import os
import time

app = Flask(__name__)
app.secret_key = "your_bt5r5rbdv5vdefesytvxVTRsecret_key_here"  # Replace with a strong secret key
DATABASE = 'users.db'

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        # Insert a test user
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
        conn.commit()
        conn.close()

init_db()

login_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Bypass this!!</title>
    <style>
      body { font-family: Arial, sans-serif; background-color: #f0f0f0; color: #333; text-align: center; }
      .container { margin-top: 100px; }
      .input-field { padding: 10px; margin: 5px; width: 250px; }
      .btn { background-color: #008cba; color: white; padding: 10px 20px; border: none; cursor: pointer; }
      .btn:hover { background-color: #005f5f; }
    </style>
</head>
<body>
  <div class="container">
    <h1>Challenge</h1>
    <p>Login using your credentials. There might be a hidden trick.</p>
    <form action="/login" method="POST">
      <input type="text" name="username" placeholder="Username" class="input-field" required><br>
      <input type="password" name="password" placeholder="Password" class="input-field" required><br>
      <button type="submit" class="btn">Login</button>
    </form>
    <p>Password Bruteforce will not work!</p>
  </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(login_template)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Intentional vulnerability: string concatenation leads to SQL injection.
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    print("Executing query:", query)

    try:
        cursor.execute(query)
        result = cursor.fetchone()
    except Exception as e:
        conn.close()
        return "An error occurred."

    conn.close()

    # Determine delay based on session cookie presence.
    # If no session cookie is sent (i.e. automated tool not handling cookies), set max delay.
    if not request.cookies.get('session'):
        delay = 5
    else:
        # Get failed_attempts from session; if not present, default to 0.
        failed_attempts = session.get('failed_attempts', 0)
        delay = min(failed_attempts, 5)

    if result:
        # Reset on success.
        session['failed_attempts'] = 0
        flag = os.environ.get('FLAG', 'FLAG_NOT_SET')
        return "Success! FLAG: " + flag
    else:
        # Increment failed_attempts and enforce delay.
        failed_attempts = session.get('failed_attempts', 0) + 1
        session['failed_attempts'] = failed_attempts
        time.sleep(delay)
        return "Login failed. Please try again."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
