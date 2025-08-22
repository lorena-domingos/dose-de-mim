from models import config


def get_diarios():
    db = config.get_db()
    return db.execute(
        "SELECT id, data, COALESCE(texto, 'Sem conteúdo') as texto FROM diario ORDER BY data DESC, id DESC").fetchall()

def insert_diarios(texto, data):
    db = config.get_db()
    return db.execute("INSERT INTO diario (texto, data) VALUES (?, ?)", (texto, data))

def delete_diario(id):
    db = config.get_db()
    db.execute("DELETE FROM diario WHERE id = ?", (id,))
    db.commit()

def atualizar_diario(novo_texto, id):
    db = config.get_db()
    db.execute("UPDATE diario SET texto = ? WHERE id = ?", (novo_texto, id))
    db.commit()

def atualizar_diario_react(novo_texto, id):
    db = config.get_db()
    db.execute("UPDATE diario SET texto = ? WHERE id = ?", (novo_texto, id))
    db.commit()