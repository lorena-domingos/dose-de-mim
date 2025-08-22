import os
from datetime import datetime
from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify, send_from_directory
from models import dados_remedios, dados_diarios, dados_medicamentos, dados_api, config
from utils import utils

main = Blueprint('main', __name__, static_folder="static", template_folder="templates")

@main.route("/", methods=["GET"])
def index():
    editando = request.args.get('editando')
    editando = int(editando) if editando else None

    remedios_db = dados_remedios.get_remedios()
    diarios_db = dados_diarios.get_diarios()
    medicamentos = dados_medicamentos.get_medicamentos()

    remedios, diarios = utils.format_data(remedios_db, diarios_db)

    return render_template("index.html", diarios=diarios, remedios=remedios, medicamentos=medicamentos,
                           editando=editando)


@main.route("/add_diario", methods=["POST"])
def add_diario():
    texto = request.form.get("texto", "").strip()
    tomou = 'remedio' in request.form
    data = request.form.get("data")

    remedio = False

    texto_diario = False

    if not data or data.strip() == "":
        data = datetime.now().strftime("%Y-%m-%d")

    if texto:
        dados_diarios.insert_diarios(texto, data)
        texto_diario = True
    if tomou and data:
        tomou_remedio = dados_remedios.select_tomou_remedio(data)
        if tomou_remedio:
            remedio = True
        else:
            dados_remedios.tomou_remedio(tomou, data)

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

    config.get_db().commit()
    return redirect(url_for("main.index"))


@main.route("/delete_diario/<int:id>")
def delete_diario(id):
    dados_diarios.delete_diario(id)
    return redirect(url_for("main.index"))


@main.route("/delete_remedio/<int:id>")
def delete_remedio(id):
    dados_remedios.delete_remedios(id)
    return redirect(url_for("main.index"))


@main.route("/add_medicamento", methods=["POST"])
def add_medicamento():
    texto = request.form.get("texto", "").strip()
    quantidade = request.form.get("quantidade", "").strip()
    dados_remedios.insert_remedio(texto, quantidade)
    return redirect(url_for("main.index"))


@main.route("/delete_medicamento/<int:id>")
def delete_medicamento(id):
    dados_medicamentos.delete_medicamento(id)
    return redirect(url_for("main.index"))


@main.route("/atualizar/<int:id>", methods=["POST"])
def atualizar_diario(id):
    novo_texto = request.form.get("texto", "").strip()
    dados_diarios.atualizar_diario(novo_texto, id)
    return redirect(url_for("main.index"))


@main.route("/api/dados", methods=["GET"])
def api_diarios():
    return dados_api.get_dados_api()

@main.route("/calendario/", defaults={"filename": "index.html"})
@main.route("/calendario/<path:filename>")
def serve_calendario(filename):
    path = os.path.join("static", "calendario")
    return send_from_directory(path, filename)

@main.route('/<path:path>')
def static_files(path):
    return send_from_directory(main.static_folder, path)


@main.route("/api/dados/<int:id>", methods=["PUT"])
def atualizar_dados(id):
    dados = request.get_json()
    novo_texto = dados.get("texto", "").strip()
    if not novo_texto:
        return jsonify({"erro": "Texto vazio"}), 400

    dados_diarios.atualizar_diario_react(novo_texto, id)
    return jsonify({"status": "sucesso", "id": id, "texto": novo_texto})


@main.route('/backup')
def backup():
    config.backup()
    return redirect(url_for("main.index"))
