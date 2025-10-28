from flask import Flask
from flask_cors import CORS
from api.devices_api import devices_api
from api.automations_api import automations_api

app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem (para testes)

# Registar blueprints
app.register_blueprint(devices_api, url_prefix="/devices")
app.register_blueprint(automations_api, url_prefix="/automations")
