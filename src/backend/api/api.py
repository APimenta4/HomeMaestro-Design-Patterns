from flask import Flask
from api.devices_api import devices_api

app = Flask(__name__)

app.register_blueprint(devices_api, url_prefix="/devices")
