from flask import Flask, render_template, request, redirect, url_for, g, flash
import sqlite3
import os, time
from datetime import datetime

app = Flask(__name__)
DATABASE = 'database.db'

app.secret_key = 'uma_senha_forte'

def init_db():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS diario (id INTEGER PRIMARY KEY AUTOINCREMENT, texto TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
            conn.execute('CREATE TABLE IF NOT EXISTS remedio (id INTEGER PRIMARY KEY AUTOINCREMENT, tomou INTEGER, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
            conn.execute('CREATE TABLE IF NOT EXISTS medicamentos (id INTEGER PRIMARY KEY AUTOINCREMENT, texto TEXT, quantidade INTEGER)')
            conn.commit()

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

    remedios_db = db.execute("SELECT id, data, tomou FROM remedio ORDER BY id DESC").fetchall()
    diarios_db = db.execute("SELECT id, data, COALESCE(texto, 'Sem conteúdo') as texto FROM diario ORDER BY id DESC").fetchall()

    remedios = []
    if remedios_db:
        for r in remedios_db:
            id, data, tomou = r
            if data != "":
                try:
                    data_obj = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    data_obj = datetime.strptime(data, '%Y-%m-%d')

                new_data = data_obj.strftime('%d/%m/%Y')
                remedios.append({"id": id, "data": new_data, "tomou": tomou})

            else:
                data_obj = None
    else:
        remedios = []

    diarios = []
    if diarios_db:
        for d in diarios_db:
            id, data, texto = d
            if data != "":
                try:
                    data_obj = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    data_obj = datetime.strptime(data, '%Y-%m-%d')

                new_data = data_obj.strftime('%d/%m/%Y')
                diarios.append({"id": id, "data": new_data, "texto": texto})

            else:
                data_obj = None
    else:
        diarios = []

    medicamentos = db.execute("SELECT id, texto, quantidade FROM medicamentos ORDER BY id DESC").fetchall()

    return render_template("index.html", diarios=diarios, remedios=remedios, medicamentos=medicamentos)

@app.route("/add_diario", methods=["POST"])
def add_diario():
    texto = request.form.get("texto")
    tomou = 'remedio' in request.form
    data = request.form.get("data")

    db = get_db()

    erro = False

    texto_diario = False

    if not data or data.strip() == "":
        data = datetime.now().strftime("%Y-%m-%d")

    if texto:
        db.execute("INSERT INTO diario (texto, data) VALUES (?, ?)", (texto, data))
        texto_diario = True
    if tomou and data:
        tomou_remedio = db.execute("SELECT id FROM remedio WHERE DATE(data) = DATE(?)", (data,)).fetchone()
        if tomou_remedio:
            erro = True
        else:
            db.execute("INSERT INTO remedio (tomou, data) VALUES (?, ?)", (tomou, data))

    if not texto and not tomou:
        flash("Preencha pelo menos um campo!", "erro")
        return redirect("/")

    if not erro:
        flash('Entrada registrada com sucesso!', "sucesso")

    if texto_diario and erro:
        flash("Diário salvo! Mas o remédio já foi registrado hoje.", "info")
    elif erro:
        flash("Você já registrou hoje!", "erro")
    elif texto_diario or tomou:
        flash("Entrada registrada com sucesso!", "sucesso")

    # remedio == erro

    db.commit()
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
    init_db()
    time.sleep(5)
    app.run(debug=True)
