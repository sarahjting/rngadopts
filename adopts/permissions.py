from adopts.models import Adopt
from rest_framework import permissions


class IsAdoptMod(permissions.IsAuthenticated):
    """
    This is specifically intended to be used for the nested adoptable resources, EG:
       /api/adopts/123/color-pools
       /api/adopts/123/color-pools/1234
       /api/adopts/123/genes
    In this example, this verifies that the logged in user has admin over adopt 123. 
    If REST framework has a way to do this natively I missed it. 
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        try:
            return Adopt.objects.get(id=view.kwargs.get('adopt_id')).mods.filter(
                pk=request.user.id).exists()
        except Adopt.DoesNotExist:
            return False
