from adopts.models import Adopt, AdoptMod
from genes.models import GenePool
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

        adopt_id = view.kwargs.get('adopt_id', None)
        gene_pool_id = view.kwargs.get('gene_pool_id', None)

        # verify that the gene pool actually belongs to the adoptable
        if gene_pool_id:
            if not GenePool.objects.filter(id=gene_pool_id, adopt_id=adopt_id).exists():
                return False

        try:
            return AdoptMod.objects.filter(adopt_id=adopt_id, mod_id=request.user.id).exists()
        except Adopt.DoesNotExist:
            return False
