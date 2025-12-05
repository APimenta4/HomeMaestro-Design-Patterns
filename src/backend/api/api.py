from flask import Flask
from flask_cors import CORS

from .automations_api import automations_api
from .devices_api import devices_api
from .integrations_api import integrations_api

app = Flask(__name__)
CORS(app)

app.register_blueprint(devices_api, url_prefix="/devices")
app.register_blueprint(automations_api, url_prefix="/automations")
app.register_blueprint(integrations_api, url_prefix="/integrations")
