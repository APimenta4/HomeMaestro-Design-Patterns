from datetime import datetime

from api.api_shared import validates_exceptions
from api.endpoint_templates import IntegrationCreationAlgorithm
from flask import Blueprint, Response, make_response, request
from integrations import IntegrationFactory
from integrations.messages import Message, MessageType
from shared import NotificationService

integrations_api = Blueprint("integrations", __name__)

notification_service = NotificationService()
integration_creation_handler = IntegrationCreationAlgorithm()


@integrations_api.route("/", methods=["GET"])
@validates_exceptions
def get_integrations() -> Response:
    integrations = [
        integration.to_dict() for integration in notification_service.integrations
    ]
    return make_response(integrations)


# Unused for now
#
# @integrations_api.route("/<int:integration_id>", methods=["GET"])
# @validates_exceptions
# def get_integration(integration_id: int) -> Response:
#     integration = home_maestro.get_integration_by_id(integration_id)
#     if not integration:
#         return make_response({"error": "Integration not found"}, 404)
#     return make_response(integration.to_dict())


@integrations_api.route("/", methods=["POST"])
@validates_exceptions
def add_integration() -> Response:
    return integration_creation_handler.create_entity(request)


@integrations_api.route("/types", methods=["GET"])
@validates_exceptions
def get_integration_types() -> Response:
    return make_response(IntegrationFactory.get_supported_integrations())


@integrations_api.route("/test", methods=["GET"])
def test_integrations():
    test_message = Message(
        message_type=MessageType.ALERT,
        content="Demonstration Notification to ensure integrations are working.",
        timestamp=datetime.now().isoformat(),
    )

    notification_service.send_notification_broadcast(test_message)
    return make_response(
        {"message": "Test notification sent to all integrations."}, 200
    )
