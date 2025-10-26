from flask import Blueprint, Response, jsonify

from home_maestro import HomeMaestro
from shared import validates_exceptions

devices_api = Blueprint("devices", __name__)

home_maestro = HomeMaestro()


@devices_api.route("/", methods=["GET"])
# @validates_exceptions
def get_devices() -> Response:
    devices = [device.to_dict() for device in home_maestro.devices]
    return jsonify(devices)
