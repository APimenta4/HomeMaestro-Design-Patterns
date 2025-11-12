# -*- coding: utf-8 -*-
from flask import Blueprint, Response, jsonify, request
from shared import validates_exceptions
from home_maestro import HomeMaestro

automations_api = Blueprint("automations", __name__)

home_maestro = HomeMaestro()


@automations_api.route("/", methods=["GET"])
@validates_exceptions
def get_automations() -> Response:
    automations = []

    for rule in home_maestro.rules:
        automations.append(
            {
                "id": str(id(rule)),
                "name": getattr(rule, "name", "Unnamed Automation"),
                "trigger_type": getattr(
                    rule.trigger, "__class__", type("Unknown")
                ).__name__,
                "action_type": getattr(
                    rule.action, "__class__", type("Unknown")
                ).__name__,
                "enabled": getattr(rule, "enabled", True),
                "description": getattr(rule, "description", ""),
            }
        )
    return jsonify(automations)


@automations_api.route("/<automation_id>", methods=["PUT"])
@validates_exceptions
def update_automation(automation_id: str) -> Response:
    data = request.get_json()
    for rule in home_maestro.rules:
        if str(id(rule)) == automation_id:
            if "enabled" in data:
                rule.enabled = data["enabled"]
            return jsonify(
                {
                    "id": automation_id,
                    "enabled": rule.enabled,
                    "message": "Automation updated",
                }
            )

    return jsonify({"error": "Automation not found"}), 404
