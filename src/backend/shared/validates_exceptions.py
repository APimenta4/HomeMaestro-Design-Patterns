from flask import Response
import functools  # ← necessário

# DESIGN PATTERN: Decorator
def validates_exceptions(api_method):
    @functools.wraps(api_method)  # ← preserva o __name__ e a docstring
    def wrapper(*args, **kwargs):
        try:
            return api_method(*args, **kwargs)
        except Exception as e:
            return Response(
                response=f"An error occurred while performing the operation: {str(e)}",
                status=500,
            )

    return wrapper
