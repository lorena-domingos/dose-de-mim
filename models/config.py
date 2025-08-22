import os, sqlite3
import dropbox
from flask import g, flash

APP_KEY = os.environ['APP_KEY']
APP_SECRET = os.environ['APP_SECRET']
REFRESH_TOKEN = os.environ['REFRESH_TOKEN']
DATABASE = 'database.db'
BACKUP = 'backups'
os.makedirs(BACKUP, exist_ok=True)


def init_db():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            conn.execute(
                'CREATE TABLE IF NOT EXISTS diario (id INTEGER PRIMARY KEY AUTOINCREMENT, texto TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
            conn.execute(
                'CREATE TABLE IF NOT EXISTS remedio (id INTEGER PRIMARY KEY AUTOINCREMENT, tomou INTEGER, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
            conn.execute(
                'CREATE TABLE IF NOT EXISTS medicamentos (id INTEGER PRIMARY KEY AUTOINCREMENT, texto TEXT, quantidade INTEGER)')
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

    if not all([APP_KEY, APP_SECRET, REFRESH_TOKEN]):
        flash("⚠️ Dropbox não configurado, backup salvo apenas local.", 'info')
        return

    try:
        dbx = dropbox.Dropbox(
            app_key=APP_KEY,
            app_secret=APP_SECRET,
            oauth2_refresh_token=REFRESH_TOKEN
        )
        with open(bk, 'rb') as f:
            dbx.files_upload(f.read(), f"/{os.path.basename(bk)}", mode=dropbox.files.WriteMode('overwrite'))
            flash("✅ Backup salvo no Dropbox também.", 'sucesso')
    except dropbox.exceptions.AuthError:
        flash("⚠️ Erro de autenticação no Dropbox, backup salvo apenas local.", 'erro')
    except Exception as e:
        flash(f"⚠️ Erro no upload para o Dropbox: {e}, backup salvo apenas local.", 'erro')


if __name__ == '__main__':
    init_db()
