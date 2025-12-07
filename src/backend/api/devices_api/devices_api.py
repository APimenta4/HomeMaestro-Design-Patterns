from api.api_shared import validates_exceptions
from api.endpoint_templates import DeviceCreationAlgorithm, HubCreationAlgorithm
from devices import DeviceStatusFactory
from devices.hubs import Hub
from flask import Blueprint, Response, make_response, request
from shared import HomeMaestro

devices_api = Blueprint("devices", __name__)

home_maestro = HomeMaestro()
device_creation_handler = DeviceCreationAlgorithm()
hub_creation_handler = HubCreationAlgorithm()


@devices_api.route("/", methods=["GET"])
@validates_exceptions
def get_devices() -> Response:
    deep = request.args.get("deep", "false").lower() == "true"
    to_dict_method = "to_dict_deep" if deep else "to_dict"

    connected = [
        getattr(device, to_dict_method)() for device in home_maestro.connected_devices
    ]
    unconnected = [
        getattr(device, to_dict_method)() for device in home_maestro.unconnected_devices
    ]
    return make_response(
        {"connected_devices": connected, "unconnected_devices": unconnected}
    )


@devices_api.route("/", methods=["POST"])
@validates_exceptions
def add_device() -> Response:
    data = request.get_json()
    if data and data.get("type"):
        return hub_creation_handler.create_entity(request)
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
    home_maestro.remove_device(device_id)

    return make_response(
        {
            "message": f"Device with ID '{device_id}' deleted successfully",
            "device_id": device_id,
        },
        200,
    )


@devices_api.route("/<int:device_id>/execute/<int:feature_id>", methods=["POST"])
@validates_exceptions
def execute_device_feature(device_id: int, feature_id: int) -> Response:
    device = home_maestro.get_device_by_id(device_id)

    if device is None:
        return make_response({"error": f"Device with id '{device_id}' not found"}, 404)

    options = request.get_json()

    try:
        # options are the keyword arguments to be passed to the feature's execute method
        device.execute_feature(feature_id, options)
    except ValueError as e:
        return make_response({"error": str(e)}, 400)

    return make_response(
        {"message": "Feature executed successfully", "device": device.to_dict_deep()},
        200,
    )


@devices_api.route("/<int:hub_id>/discover", methods=["POST"])
@validates_exceptions
def discover_devices(hub_id: int) -> Response:
    hub = home_maestro.get_device_by_id(hub_id)

    if hub is None or not isinstance(hub, Hub):
        return make_response({"error": f"Hub with id '{hub_id}' not found"}, 404)

    hub.discover_devices()

    return make_response(
        {"message": f"Discovery process started for hub '{hub.name}'"}, 200
    )


@devices_api.route("/<int:hub_id>/unpair/<int:device_id>", methods=["POST"])
@validates_exceptions
def unpair_device(hub_id: int, device_id: int) -> Response:
    hub = home_maestro.get_device_by_id(hub_id)

    if hub is None or not isinstance(hub, Hub):
        return make_response({"error": f"Hub with id '{hub_id}' not found"}, 404)

    device = home_maestro.get_device_by_id(device_id)

    if device is None:
        return make_response({"error": f"Device with id '{device_id}' not found"}, 404)

    hub.unpair_device(device)

    return make_response(
        {
            "message": f"Successfully unpaired device '{device.name}' from hub '{hub.name}'",
            "hub_id": hub_id,
            "device_id": device_id,
        },
        200,
    )
