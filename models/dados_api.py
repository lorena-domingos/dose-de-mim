from models import config
from flask import jsonify

def get_dados_api():
    db = config.get_db()
    diarios_db = db.execute(
        "SELECT id, data, COALESCE(texto, 'Sem conteúdo') as texto FROM diario ORDER BY data DESC").fetchall()
    remedios_db = db.execute("SELECT id, data, tomou FROM remedio ORDER BY data DESC").fetchall()
    diarios = [{"id": d["id"], "date": d["data"], "texto": d["texto"]} for d in diarios_db]
    remedios = [{"data": r["data"], "tomou": r["tomou"]} for r in remedios_db]
    return jsonify({"diarios": diarios, "remedios": remedios})