
from rest_framework.response import Response
from rest_framework import status

# lol I wrote this before realising REST framework has an equivalent... might use it later so let's keep


def find_or_fail(model, var_name, key='pk'):
    def decorator(view_fn):
        def wrapper(*args, **kwargs):
            try:
                kwargs[var_name] = model.objects.get(id=kwargs[key])
            except model.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return view_fn(*args, **kwargs)
        return wrapper
    return decorator
