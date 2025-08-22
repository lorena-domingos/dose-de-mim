from models import config


def get_medicamentos():
    db = config.get_db()
    return db.execute("SELECT id, texto, quantidade FROM medicamentos ORDER BY id DESC").fetchall()

def delete_medicamento(id):
    db = config.get_db()
    db.execute("DELETE FROM medicamentos WHERE id = ?", (id,))
    db.commit()