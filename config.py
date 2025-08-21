import os, sqlite3
import dropbox
from flask import g

MY_TOKEN = os.environ['Dropbox']
DATABASE = 'database.db'
BACKUP = 'backups'
os.makedirs(BACKUP, exist_ok=True)

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

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
def init_app(app):
    app.teardown_appcontext(close_connection)

def backup():
    bk = os.path.join(BACKUP, f'database.db')
    db = get_db()
    backup_db = sqlite3.connect(bk)

    with backup_db:
        db.backup(backup_db)

    backup_db.close()

    dbx = dropbox.Dropbox(MY_TOKEN)
    with open(bk, 'rb') as f:
        dbx.files_upload(f.read(), f"/{os.path.basename(bk)}", mode=dropbox.files.WriteMode('overwrite'))

    return bk

if __name__ == '__main__':
    init_db()
    