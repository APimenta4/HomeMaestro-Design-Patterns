# devices_api.py
# -*- coding: utf-8 -*-
from devices import Device, DeviceStatus
from devices.features import LampFeature
from devices.hubs import ZigbeeHub, ZWaveHub
from flask import Blueprint, Response, make_response, request
from home_maestro import HomeMaestro
from shared import validates_exceptions

devices_api = Blueprint("devices", __name__)

home_maestro = HomeMaestro()


@devices_api.route("/", methods=["GET"])
@validates_exceptions
def get_devices() -> Response:
    devices = [device.to_dict() for device in home_maestro.devices]
    return make_response(devices)


@devices_api.route("/", methods=["POST"])
@validates_exceptions
def add_device() -> Response:
    """Adicionar novo device"""

    data = request.get_json()
    if not data:
        return make_response("Missing device data", 400)

    name = data.get("name")
    type_ = data.get("type")
    status_str = data.get("status", "offline").lower()
    status = (
        DeviceStatus[status_str]
        if status_str in DeviceStatus.__members__
        else DeviceStatus.OFFLINE
    )

    # Criar device genérico ou hub conforme tipo
    # TODO: fix type creation logic. suggestion: factory pattern
    if type_ == "ZWaveHub":
        new_device = ZWaveHub(name, status)
    elif type_ == "ZigbeeHub":
        new_device = ZigbeeHub(name, status)
    else:
        # Para outros tipos, podemos usar LampFeature como exemplo
        features = set()
        if type_ == "Light":
            features.add(LampFeature("Default Light Feature", {"max_brightness": 100}))
        new_device = Device(name, status, features)

    home_maestro.add_device(new_device)

    return make_response(
        {"message": "Device added successfully", "device": new_device.to_dict()}, 201
    )
