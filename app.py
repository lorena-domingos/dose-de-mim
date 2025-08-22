from flask import Flask
from flask_cors import CORS
import time
from models import config
from controllers.routes import main

app = Flask(__name__)
app.secret_key = "uma_senha_forte"
CORS(app)

config.init_app(app)

app.register_blueprint(main)

if __name__ == "__main__":
    config.init_db()
    time.sleep(5)
    app.run(debug=True)
