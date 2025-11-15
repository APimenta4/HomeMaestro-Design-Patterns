import functools
import logging

from flask import Response

logger = logging.getLogger(__name__)


# DESIGN PATTERN: Decorator
def validates_exceptions(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Exception as e:
            logger.error("An error occurred: %s", e, exc_info=True)
            return Response(
                response=f"An error occurred while performing the operation: {str(e)}",
                status=500,
            )

    return wrapper
