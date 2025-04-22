# app.py
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create DB table if it doesn't exist
def create_database():
    conn = sqlite3.connect("specimens.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            observed_size REAL,
            magnification REAL,
            actual_size REAL
        )
    """)
    conn.commit()
    conn.close()

# Save entry to DB
def save_to_database(username, observed, magnification, actual):
    conn = sqlite3.connect("specimens.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO results (username, observed_size, magnification, actual_size)
        VALUES (?, ?, ?, ?)
    """, (username, observed, magnification, actual))
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
            username = request.form["username"]
            observed = float(request.form["observed"])
            magnification = float(request.form["magnification"])

            if magnification == 0:
                error = "Magnification cannot be zero."
            else:
                actual = observed / magnification
                save_to_database(username, observed, magnification, actual)
                result = f"{actual:.4f} mm"
        except ValueError:
            error = "Please enter valid numeric values."

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    create_database()
    app.run(debug=True)


import os
port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT isn’t set
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)