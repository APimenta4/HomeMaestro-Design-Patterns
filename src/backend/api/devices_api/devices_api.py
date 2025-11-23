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


@devices_api.route("/<device_id>", methods=["GET"])
@validates_exceptions
def get_device_details(device_id: str) -> Response:
    print(f"Looking for device with ID: {device_id} (type: {type(device_id)})")
    print(f"Available devices: {[(d.id, d.name, type(d.id)) for d in home_maestro.devices]}")
    
    device = None
    for d in home_maestro.devices:
        print(f"Comparing {d.id} == {device_id}: {d.id == device_id}")
        if str(d.id) == str(device_id):  # Explicit string comparison
            device = d
            break
    
    if device is None:
        print(f"Device not found!")
        return make_response(
            {"error": f"Device with id '{device_id}' not found"},
            404
        )
    
    print(f"Found device: {device.name}")
    return make_response(device.to_dict_deep(), 200)

@devices_api.route("/<device_id>", methods=["PUT"])
@validates_exceptions
def update_device(device_id: str) -> Response:
    device = None
    for d in home_maestro.devices:
        if d.id == device_id:
            device = d
            break
    
    if device is None:
        return make_response(
            {"error": f"Device with id '{device_id}' not found"},
            404
        )
    
    data = request.get_json()
    
    if not data:
        return make_response(
            {"error": "No data provided"},
            400
        )
    
    if "name" in data:
        new_name = data["name"]
        if not new_name or not isinstance(new_name, str):
            return make_response(
                {"error": "Invalid name"},
                400
            )
        device.name = new_name.strip()
    
    if "status" in data:
        try:
            from devices.device import DeviceStatus
            new_status = data["status"]
            device.status = DeviceStatus(new_status.lower())
        except ValueError:
            return make_response(
                {"error": f"Invalid status. Must be one of: online, offline, error"},
                400
            )
    
    return make_response(device.to_dict_deep(), 200)


@devices_api.route("/<device_id>", methods=["DELETE"])
@validates_exceptions
def delete_device(device_id: str) -> Response:
    device = None
    for d in home_maestro.devices:
        if d.id == device_id:
            device = d
            break
    
    if device is None:
        return make_response(
            {"error": f"Device with id '{device_id}' not found"},
            404
        )
    
    home_maestro.devices.remove(device)
    
    return make_response(
        {
            "message": f"Device '{device.name}' deleted successfully",
            "device_id": device_id
        },
        200
    )