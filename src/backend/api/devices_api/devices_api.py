# devices_api.py
# -*- coding: utf-8 -*-
from flask import Blueprint, Response, jsonify, request
from shared import validates_exceptions

from devices.device import Device, DeviceStatus
from devices.features import LampFeature
from devices.hubs import ZWaveHub, ZigbeeHub

devices_api = Blueprint("devices", __name__)

# Referência ao HomeMaestro
home_maestro = None

def init_home_maestro(hm):
    """Inicializar a referência ao HomeMaestro"""
    global home_maestro
    home_maestro = hm

@devices_api.route("/", methods=["GET"])
@validates_exceptions
def get_devices() -> Response:
    devices_list = []
    for device in home_maestro.devices:
        # Status
        status_value = getattr(device, "status", None)
        status_str = status_value.name if hasattr(status_value, "name") else str(status_value or "Unknown")

        # Features
        features = []
        if hasattr(device, "features"):
            for f in device.features:
                features.append({
                    "name": getattr(f, "name", "Unknown Feature"),
                    "properties": getattr(f, "properties", {})
                })

        # Device dict completo
        device_dict = {
            "name": getattr(device, "name", "Unnamed Device"),
            "type": device.__class__.__name__,
            "status": status_str,
            "features": features
        }

        devices_list.append(device_dict)

    return jsonify(devices_list)



@devices_api.route("/", methods=["POST"])
@validates_exceptions
def add_device() -> Response:
    """Adicionar novo device"""
    if not home_maestro:
        return jsonify({"error": "HomeMaestro not initialized"}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing device data"}), 400

    name = data.get("name")
    type_ = data.get("type")
    status_str = data.get("status", "offline").upper()
    status = DeviceStatus[status_str] if status_str in DeviceStatus.__members__ else DeviceStatus.OFFLINE

    # Criar device genérico ou hub conforme tipo
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

    return jsonify({
        "message": "Device added successfully",
        "device": {
            "name": new_device.name,
            "type": new_device.__class__.__name__,
            "status": new_device.status.name
        }
    }), 201
