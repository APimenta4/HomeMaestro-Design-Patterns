from api.api_shared import validates_exceptions
from api.endpoint_templates import DeviceCreationAlgorithm
from devices import DeviceStatusFactory
from flask import Blueprint, Response, make_response, request
from shared import HomeMaestro

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


@devices_api.route("/<int:device_id>", methods=["GET"])
@validates_exceptions
def get_device_details(device_id: int) -> Response:
    device = home_maestro.get_device_by_id(device_id)

    if device is None:
        return make_response({"error": f"Device with id '{device_id}' not found"}, 404)

    return make_response(device.to_dict_deep(), 200)


@devices_api.route("/<int:device_id>", methods=["PUT"])
@validates_exceptions
def update_device(device_id: int) -> Response:
    device = home_maestro.get_device_by_id(device_id)

    if device is None:
        return make_response({"error": f"Device with id '{device_id}' not found"}, 404)

    data = request.get_json()

    if not data:
        return make_response({"error": "No data provided"}, 400)

    if "name" in data:
        new_name = data["name"]
        if not new_name or not isinstance(new_name, str):
            return make_response({"error": "Invalid name"}, 400)
        device.name = new_name.strip()

    if "status" in data:
        try:
            device.status = DeviceStatusFactory.create_status(data["status"])
        except ValueError:
            return make_response(
                {"error": "Invalid status. Must be one of: online, offline, error"},
                400,
            )

    return make_response(device.to_dict_deep(), 200)


@devices_api.route("/<int:device_id>", methods=["DELETE"])
@validates_exceptions
def delete_device(device_id: int) -> Response:
    device = home_maestro.get_device_by_id(device_id)

    if device is None:
        return make_response({"error": f"Device with id '{device_id}' not found"}, 404)

    home_maestro.devices.remove(device)

    return make_response(
        {
            "message": f"Device '{device.name}' deleted successfully",
            "device_id": device_id,
        },
        200,
    )


@devices_api.route("/<int:device_id>/execute", methods=["POST"])
@validates_exceptions
def execute_device_feature(device_id: int) -> Response:
    device = home_maestro.get_device_by_id(device_id)

    if device is None:
        return make_response({"error": f"Device with id '{device_id}' not found"}, 404)

    # TODO: Implement
    pass
