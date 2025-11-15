import logging
from abc import ABC, abstractmethod
from typing import Any

from flask import Request, Response, make_response

from shared import Identifiable

logger = logging.getLogger(__name__)


# DESIGN PATTERN: Template Method
# reduces boilerplate steps
# enforce strict algorithm
# in the future, we can add steps like persist in database
class EntityCreationAlgorithm(ABC):

    def create_entity(self, request: Request) -> Response:
        payload = self.parse_payload(request)
        self.validate_fields(payload)  # Partially hooked method
        prepared_data = self.prepare_input_data(payload)  # Hooked method
        entity = self.instantiate_and_persist_entity(prepared_data)  # Hooked method
        return self.success_response(entity)

    def parse_payload(self, payload: Request) -> dict[str, object]:
        try:
            request = payload.get_json()
        except Exception as e:
            raise ValueError("Payload is not valid JSON") from e
        if not request:
            raise ValueError("Payload is empty")
        return request

    def validate_fields(self, payload: dict[str, Any]) -> bool:
        required_fields = self.required_fields()
        optional_fields = self.optional_fields()

        for field, expected_type in required_fields.items():
            if field not in payload:
                raise ValueError(f"Missing required field: '{field}'")

            if not isinstance(payload[field], expected_type):
                raise ValueError(
                    f"Required field '{field}' must be of type {expected_type.__name__}"
                )

            if payload[field] is None or len(payload[field]) == 0:
                raise ValueError(f"Field '{field}' cannot be empty.")

            if expected_type == str and not payload[field].strip():
                raise ValueError(f"Field '{field}' cannot be empty or whitespace.")

        optional_fields = {"type": str, "features": list}
        for field, expected_type in optional_fields.items():
            if field in payload and not isinstance(payload[field], expected_type):
                raise ValueError(
                    f"Optional field '{field}' must be of type {expected_type.__name__}. "
                    "Either omit it or provide a valid value type."
                )

            if payload.get(field) and len(payload[field]) == 0:
                payload.pop(field)
                logger.warning("Optional field '%s' is empty. Ignoring field.", field)

            if (
                field in payload
                and expected_type == str
                and not (payload[field] or "").strip()
            ):
                payload.pop(field)
                logger.warning(
                    "Optional field '%s' is empty or whitespace. Ignoring field.", field
                )

        return True

    @abstractmethod
    def required_fields(self) -> dict[str, type]:  # Hooked method
        pass

    @abstractmethod
    def optional_fields(self) -> dict[str, type]:  # Hooked method
        pass

    @abstractmethod
    def prepare_input_data(self, payload: dict[str, object]) -> dict[str, object]:
        pass

    @abstractmethod
    def instantiate_and_persist_entity(
        self, prepared_data: dict[str, object]
    ) -> Identifiable:
        pass

    def success_response(self, entity: Identifiable):
        return make_response(
            {
                "message": f"{entity.__class__.__name__} added successfully",
                f"{entity.__class__.__name__.lower()}": entity.to_dict(),
            },
            201,
        )
