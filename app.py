from flask import Flask, render_template, request, redirect, url_for, g, flash
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

app.secret_key = 'uma_senha_forte'

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

@app.route("/", methods=["GET"])
def index():
    db = get_db()
    diarios = db.execute("SELECT id, data, COALESCE(texto, 'Sem conteúdo') as texto, emoji FROM diario ORDER BY id DESC").fetchall()
    remedios = db.execute("SELECT id, data, tomou FROM remedio ORDER BY id DESC").fetchall()
    medicamentos = db.execute("SELECT id, texto, quantidade FROM medicamentos ORDER BY id DESC").fetchall()

    return render_template("index.html", diarios=diarios, remedios=remedios, medicamentos=medicamentos)

@app.route("/add_diario", methods=["POST"])
def add_diario():
    texto = request.form.get("texto")
    humor = request.form.get("humor")
    tomou = 'remedio' in request.form

    db = get_db()

    if texto and humor:
        db.execute("INSERT INTO diario (texto, emoji) VALUES (?, ?)", (texto, humor))
    elif humor:
        db.execute("INSERT INTO diario (emoji) VALUES (?)", (humor,))
    elif texto:
        db.execute("INSERT INTO diario (texto) VALUES (?)", (texto,))

    if tomou:
        db.execute("INSERT INTO remedio (tomou) VALUES (?)", (tomou,))

    if not texto and not humor and not tomou:
        flash("Preencha pelo menos um campo!", "erro")
        return redirect("/")

    db.commit()
    flash('Entrada registrada com sucesso!')
    return redirect("/")

@app.route("/delete_diario/<int:id>")
def delete_diario(id):
    db = get_db()
    db.execute("DELETE FROM diario WHERE id = ?", (id,))
    db.commit()
    return redirect("/")

@app.route("/delete_remedio/<int:id>")
def delete_remedio(id):
    db = get_db()
    db.execute("DELETE FROM remedio WHERE id = ?", (id,))
    db.commit()
    return redirect("/")

@app.route("/add_medicamento", methods=["POST"])
def add_medicamento():
    texto = request.form["texto"]
    quantidade = request.form["quantidade"]
    db = get_db()
    db.execute("INSERT INTO medicamentos (texto, quantidade) VALUES (?, ?)", (texto, quantidade))
    db.commit()
    return redirect("/")

@app.route("/delete_medicamento/<int:id>")
def delete_medicamento(id):
    db = get_db()
    db.execute("DELETE FROM medicamentos WHERE id = ?", (id,))
    db.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
