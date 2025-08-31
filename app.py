from flask import Flask, request, render_template_string
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv('DB_HOST', 'mysql'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'root'),
            database=os.getenv('DB_NAME', 'flaskdb')
        )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.before_first_request
def init_db():
    db = get_db_connection()
    if db:
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100))")
        db.commit()
        cursor.close()
        db.close()

# Simple HTML form
html = """
<!doctype html>
<title>Flask MySQL App</title>
<h2>Enter Your Name</h2>
<form method="POST">
  <input type="text" name="username">
  <input type="submit" value="Submit">
</form>
<ul>
{% for user in users %}
  <li>{{ user }}</li>
{% endfor %}
</ul>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db_connection()
    if not db:
        return "Database connection error", 500
    
    cursor = db.cursor()
    try:
        if request.method == "POST":
            username = request.form["username"]
            cursor.execute("INSERT INTO users (name) VALUES (%s)", (username,))
            db.commit()
        
        cursor.execute("SELECT name FROM users")
        users = [row[0] for row in cursor.fetchall()]
        return render_template_string(html, users=users)
    except Error as e:
        return f"Database error: {e}", 500
    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
