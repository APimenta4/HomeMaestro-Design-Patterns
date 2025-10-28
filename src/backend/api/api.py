from flask import Flask
from flask_cors import CORS
from api.devices_api import devices_api

app = Flask(__name__)
CORS(app)

app.register_blueprint(devices_api, url_prefix="/devices")
