from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        texto = request.form.get("texto")
        humor = request.form.get("humor")
        tomou = 'remedio' in request.form

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO diario (texto, emoji) VALUES (?, ?)", (texto, humor))
        cursor.execute("INSERT INTO remedio (tomou) VALUES (?)", (int(tomou),))
        conn.commit()
        conn.close()
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)