from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="mysql",
    user="root",
    password="root",
    database="flaskdb"
)

cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100))")

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
    if request.method == "POST":
        username = request.form["username"]
        cursor.execute("INSERT INTO users (name) VALUES (%s)", (username,))
        db.commit()
    cursor.execute("SELECT name FROM users")
    users = [row[0] for row in cursor.fetchall()]
    return render_template_string(html, users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
