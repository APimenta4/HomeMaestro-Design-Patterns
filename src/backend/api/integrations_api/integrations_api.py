from api.api_shared import validates_exceptions
from api.endpoint_templates import IntegrationCreationAlgorithm
from flask import Blueprint, Response, make_response, request
from shared import HomeMaestro

integrations_api = Blueprint("integrations", __name__)

home_maestro = HomeMaestro()
integration_creation_handler = IntegrationCreationAlgorithm()


@integrations_api.route("/", methods=["GET"])
@validates_exceptions
def get_integrations() -> Response:
    print("Fetching integrations")
    print(home_maestro.notification_service.integrations)
    integrations = [
        integration.to_dict()
        for integration in home_maestro.notification_service.integrations
    ]
    return make_response(integrations)


@integrations_api.route("/<int:integration_id>", methods=["GET"])
@validates_exceptions
def get_integration(integration_id: int) -> Response:
    integration = home_maestro.get_integration_by_id(integration_id)
    if not integration:
        return make_response({"error": "Integration not found"}, 404)
    return make_response(integration.to_dict())


@integrations_api.route("/", methods=["POST"])
@validates_exceptions
def add_integration() -> Response:
    return integration_creation_handler.create_entity(request)