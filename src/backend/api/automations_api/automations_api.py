# -*- coding: utf-8 -*-
from flask import Blueprint, Response, jsonify, request
from api.api_shared import validates_exceptions
from api.endpoint_templates import AutomationCreationAlgorithm
from home_maestro import HomeMaestro

automations_api = Blueprint("automations", __name__)

home_maestro = HomeMaestro()

automation_creation_handler = AutomationCreationAlgorithm()


@automations_api.route("/", methods=["GET"])
@validates_exceptions
def get_automations() -> Response:
    automations = []

    for automation in home_maestro.automations:
        automations.append(
            {
                "id": str(id(automation)),
                "name": getattr(automation, "name", "Unnamed Automation"),
                "trigger_type": getattr(
                    automation.trigger, "__class__", type("Unknown")
                ).__name__,
                "action_type": getattr(
                    automation.action, "__class__", type("Unknown")
                ).__name__,
                "enabled": getattr(automation, "enabled", True),
                "description": getattr(automation, "description", ""),
            }
        )
    return jsonify(automations)

    # devices = [device.to_dict() for device in home_maestro.devices]
    # return make_response(devices)


@automations_api.route("/<automation_id>", methods=["PUT"])
@validates_exceptions
def toggle_automation(automation_id: str) -> Response:
    data = request.get_json()
    for automation in home_maestro.automations:
        if str(id(automation)) == automation_id:
            if "enabled" in data:
                automation.enabled = data["enabled"]

            return jsonify(
                {
                    "id": automation_id,
                    "enabled": automation.enabled,
                    "message": "Automation updated",
                }
            )

    return jsonify({"error": "Automation not found"}), 404


@automations_api.route("/", methods=["POST"])
@validates_exceptions
def add_automation() -> Response:
    return automation_creation_handler.create_entity(request)
