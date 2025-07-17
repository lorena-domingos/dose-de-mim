from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, timeout=10)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        texto = request.form.get("texto")
        humor = request.form.get("humor")
        tomou = 'remedio' in request.form

        db = get_db()
        db.execute("INSERT INTO diario (texto, emoji) VALUES (?, ?)", (texto, humor))
        db.execute("INSERT INTO remedio (tomou) VALUES (?)", (tomou,))
        db.commit()

        return redirect(url_for("index"))

    db = get_db()
    diarios = db.execute("SELECT id, data, texto, emoji FROM diario ORDER BY id DESC").fetchall()
    remedios = db.execute("SELECT data, tomou FROM remedio ORDER BY id DESC").fetchall()

    return render_template("index.html", diarios=diarios, remedios=remedios)


@app.route("/delete_diario/<int:id>")
def delete_diario(id):
    db = get_db()
    db.execute("DELETE FROM diario WHERE id = ?", (id,))
    db.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
