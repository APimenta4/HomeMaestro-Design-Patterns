# DESIGN PATTERN: Decorator
import functools


def append_type(to_dict_method):
    @functools.wraps(to_dict_method)
    def wrapper(self, *args, **kwargs):
        result = to_dict_method(self, *args, **kwargs)
        result["type"] = self.__class__.__name__
        return result

    return wrapper
