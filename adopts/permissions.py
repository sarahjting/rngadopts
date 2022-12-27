from adopts.models import Adopt
from rest_framework import permissions

# I actually didn't end up using this (decided I'd prefer to do the filter on the query), but it might be useful later


class IsAdoptMod(permissions.IsAuthenticated):
    """
    Object-level permission to only allow mods of an adopt to edit it.
    The model instance must either be an Adopt, or have an `adopt` attribute on it. 
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if isinstance(obj, Adopt):
            adopt = obj
        elif hasattr(obj, 'adopt'):
            adopt = obj.adopt
        else:
            return False

        return adopt.mods.filter(pk=request.user.id).exists()
