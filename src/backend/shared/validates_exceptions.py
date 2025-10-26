from flask import Response


# DESIGN PATTERN: Decorator
def validates_exceptions(api_method):

    def wrapper(*args, **kwargs):
        try:
            return api_method(*args, **kwargs)
        except Exception as e:
            return Response(
                response=f"An error occurred while performing the operation: {str(e)}",
                status=500,
            )

    return wrapper
