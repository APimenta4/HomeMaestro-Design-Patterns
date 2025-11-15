# devices_api.py
# -*- coding: utf-8 -*-
from flask import Blueprint, Response, make_response, request

from api.api_shared import validates_exceptions
from api.endpoint_templates import DeviceCreationAlgorithm
from home_maestro import HomeMaestro

devices_api = Blueprint("devices", __name__)

home_maestro = HomeMaestro()
device_creation_handler = DeviceCreationAlgorithm()


@devices_api.route("/", methods=["GET"])
@validates_exceptions
def get_devices() -> Response:
    devices = [device.to_dict() for device in home_maestro.devices]
    return make_response(devices)


@devices_api.route("/", methods=["POST"])
@validates_exceptions
def add_device() -> Response:
    return device_creation_handler.create_entity(request)
