from typing import Any

from api.endpoint_templates import EntityCreationAlgorithm
from integrations import IntegrationFactory
from shared import NotificationService

notification_service = NotificationService()


class IntegrationCreationAlgorithm(EntityCreationAlgorithm):

    def required_fields(self) -> dict[str, type]:
        return {"type": str}

    def optional_fields(self) -> dict[str, type]:
        return {"webhook_url": str}

    def prepare_input_data(self, payload: dict[str, Any]) -> dict[str, object]:
        # No preparation needed for now
        return payload

    def instantiate_and_persist_entity(self, prepared_data: dict[str, Any]):
        integration = IntegrationFactory.create_integration(**prepared_data)
        notification_service.add_integration(integration)
        return integration
