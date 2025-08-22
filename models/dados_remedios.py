from models import config


def get_remedios():
    db = config.get_db()
    return db.execute("SELECT id, data, tomou FROM remedio ORDER BY data DESC").fetchall()


def delete_remedios(id):
    db = config.get_db()
    db.execute("DELETE FROM remedio WHERE id = ?", (id,))
    db.commit()


def insert_remedio(texto, quantidade):
    db = config.get_db()
    db.execute("INSERT INTO medicamentos (texto, quantidade) VALUES (?, ?)", (texto, quantidade))
    db.commit()

def select_tomou_remedio(data):
    db = config.get_db()
    return db.execute("SELECT id FROM remedio WHERE DATE(data) = DATE(?)", (data,)).fetchone()

def tomou_remedio(tomou, data):
    db = config.get_db()
    return db.execute("INSERT INTO remedio (tomou, data) VALUES (?, ?)", (tomou, data))
