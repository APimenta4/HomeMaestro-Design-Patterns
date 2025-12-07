# -*- coding: utf-8 -*-
from api.api_shared import validates_exceptions
from api.endpoint_templates import AutomationCreationAlgorithm
from flask import Blueprint, Response, jsonify, make_response, request
from shared import HomeMaestro

automations_api = Blueprint("automations", __name__)

home_maestro = HomeMaestro()

automation_creation_handler = AutomationCreationAlgorithm()


@automations_api.route("/", methods=["GET"])
@validates_exceptions
def get_automations() -> Response:
    automations = [automation.to_dict() for automation in home_maestro.automations]
    return make_response(automations)


@automations_api.route("/<int:automation_id>", methods=["GET"])
@validates_exceptions
def get_automation_details(automation_id: int) -> Response:
    automation = home_maestro.get_automation_by_id(automation_id)

    if automation is None:
        return make_response({"error": f"Automation with id '{automation_id}' not found"}, 404)

    return make_response(automation.to_dict_deep(), 200)


@automations_api.route("/<int:automation_id>", methods=["PATCH"])
@validates_exceptions
def toggle_automation(automation_id: int) -> Response:
    data = request.get_json()
    automation = home_maestro.get_automation_by_id(automation_id)
    if not automation:
        return make_response(jsonify({"error": "Automation not found"}), 404)
    if "enabled" in data:
        automation.enabled = data["enabled"]
    return make_response(automation.to_dict())


@automations_api.route("/", methods=["POST"])
@validates_exceptions
def add_automation() -> Response:
    return automation_creation_handler.create_entity(request)
