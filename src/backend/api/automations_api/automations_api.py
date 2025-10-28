# -*- coding: utf-8 -*-
from flask import Blueprint, Response, jsonify, request
from shared import validates_exceptions

automations_api = Blueprint("automations", __name__)

# Referência ao HomeMaestro
home_maestro = None

def init_home_maestro(hm):
    """Inicializar a referencia ao HomeMaestro"""
    global home_maestro
    home_maestro = hm

@automations_api.route("/", methods=["GET"])
@validates_exceptions
def get_automations() -> Response:
    if not home_maestro:
        return jsonify({"error": "HomeMaestro not initialized"}), 500
    
    automations = []
    if hasattr(home_maestro, 'rules'):
        for rule in home_maestro.rules:
            automations.append({
                "id": str(id(rule)),
                "name": getattr(rule, 'name', 'Unnamed Automation'),
                "trigger_type": getattr(rule.trigger, "__class__", type("Unknown")).__name__,
                "action_type": getattr(rule.action, "__class__", type("Unknown")).__name__,
                "enabled": getattr(rule, 'enabled', True),
                "description": getattr(rule, 'description', '')
            })
    return jsonify(automations)

@automations_api.route("/<automation_id>", methods=["PUT"])
@validates_exceptions
def update_automation(automation_id: str) -> Response:
    if not home_maestro:
        return jsonify({"error": "HomeMaestro not initialized"}), 500
    
    data = request.get_json()
    for rule in home_maestro.rules:
        if str(id(rule)) == automation_id:
            if "enabled" in data:
                rule.enabled = data["enabled"]
            return jsonify({"id": automation_id, "enabled": rule.enabled, "message": "Automation updated"})
    
    return jsonify({"error": "Automation not found"}), 404
