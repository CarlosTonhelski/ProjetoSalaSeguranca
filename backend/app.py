from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db

# BLUEPRINTS
from routes.auth_routes import auth_bp
from routes.colaborador_routes import colaborador_bp
from routes.monitoramento_routes import monitoramento_bp
from routes.rfid_routes import rfid_bp
from routes.export_routes import export_bp

# FLASK
app = Flask(__name__)

# CONFIG
app.config.from_object(Config)

# CORS
CORS(app)

# DATABASE
db.init_app(app)

# REGISTRAR BLUEPRINTS
app.register_blueprint(auth_bp)

app.register_blueprint(colaborador_bp)

app.register_blueprint(monitoramento_bp)

app.register_blueprint(rfid_bp)

app.register_blueprint(export_bp)

# HOME
@app.route('/')
def home():

    return {
        'mensagem': 'Backend funcionando'
    }

# START
if __name__ == '__main__':

    print('Iniciando servidor...')

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False
    )