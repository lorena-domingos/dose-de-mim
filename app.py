from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import time
import utils
import config

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'uma_senha_forte'
CORS(app)

config.init_app(app)

@app.route("/", methods=["GET"])
def index():
    editando = request.args.get('editando')
    editando = int(editando) if editando else None
    
    db = config.get_db()
    
    remedios_db = db.execute("SELECT id, data, tomou FROM remedio ORDER BY data DESC").fetchall()
    diarios_db = db.execute("SELECT id, data, COALESCE(texto, 'Sem conteúdo') as texto FROM diario ORDER BY data DESC").fetchall()
    remedios, diarios = utils.format_data(remedios_db, diarios_db)
    
    medicamentos = db.execute("SELECT id, texto, quantidade FROM medicamentos ORDER BY id DESC").fetchall()

    return render_template("index.html", diarios=diarios, remedios=remedios, medicamentos=medicamentos, editando=editando)

@app.route("/add_diario", methods=["POST"])
def add_diario():
    texto = request.form.get("texto", "").strip()
    tomou = 'remedio' in request.form
    data = request.form.get("data")

    db = config.get_db()

    remedio = False

    texto_diario = False

    if not data or data.strip() == "":
        data = datetime.now().strftime("%Y-%m-%d")

    if texto:
        db.execute("INSERT INTO diario (texto, data) VALUES (?, ?)", (texto, data))
        texto_diario = True
    if tomou and data:
        tomou_remedio = db.execute("SELECT id FROM remedio WHERE DATE(data) = DATE(?)", (data,)).fetchone()
        if tomou_remedio:
            remedio = True
        else:
            db.execute("INSERT INTO remedio (tomou, data) VALUES (?, ?)", (tomou, data))

    if not texto and not tomou:
        flash("Preencha pelo menos um campo!", "erro")
        return redirect("/")

    if not remedio:
        flash('Entrada registrada com sucesso!', "sucesso")

    if texto_diario and remedio:
        flash("Diário salvo! Mas o remédio já foi registrado hoje.", "info")
    elif remedio:
        flash("Você já registrou hoje!", "erro")
    elif texto_diario or tomou:
        flash("Entrada registrada com sucesso!", "sucesso")

    db.commit()
    return redirect(url_for("index"))

@app.route("/delete_diario/<int:id>")
def delete_diario(id):
    db = config.get_db()
    db.execute("DELETE FROM diario WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("index"))

@app.route("/delete_remedio/<int:id>")
def delete_remedio(id):
    db = config.get_db()
    db.execute("DELETE FROM remedio WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("index"))

@app.route("/add_medicamento", methods=["POST"])
def add_medicamento():
    texto = request.form.get("texto", "").strip()
    quantidade = request.form.get("quantidade", "").strip()
    db = config.get_db()
    db.execute("INSERT INTO medicamentos (texto, quantidade) VALUES (?, ?)", (texto, quantidade))
    db.commit()
    return redirect(url_for("index"))

@app.route("/delete_medicamento/<int:id>")
def delete_medicamento(id):
    db = config.get_db()
    db.execute("DELETE FROM medicamentos WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("index"))

@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar_diario(id):
    novo_texto = request.form.get("texto", "").strip()
    
    db = config.get_db()
    db.execute("UPDATE diario SET texto = ? WHERE id = ?", (novo_texto, id))
    db.commit()
    return redirect(url_for("index"))

@app.route("/api/dados", methods=["GET"])
def api_diarios():
    db = config.get_db()
    diarios_db = db.execute("SELECT id, data, COALESCE(texto, 'Sem conteúdo') as texto FROM diario ORDER BY data DESC").fetchall()
    remedios_db = db.execute("SELECT id, data, tomou FROM remedio ORDER BY data DESC").fetchall()
    diarios = [{"id": d["id"], "date": d["data"], "texto": d["texto"]} for d in diarios_db]
    remedios = [{"data": r["data"], "tomou": r["tomou"]} for r in remedios_db]
    return jsonify({"diarios":diarios, "remedios":remedios})

@app.route('/calendario')
def serve_calendario():
    return send_from_directory('static/calendario', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    config.init_db()
    time.sleep(5)
    app.run(debug=True)
