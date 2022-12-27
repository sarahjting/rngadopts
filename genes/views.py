from adopts.permissions import IsAdoptMod
from genes.serializers import GenePoolSerializer, GeneSerializer
from genes.models import GenePool, Gene
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.response import Response
from users.mixins import ApiLoginRequiredMixin


class GenePoolApiView(generics.ListCreateAPIView):
    serializer_class = GenePoolSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return GenePool.objects.filter(adopt_id=self.kwargs.get('adopt_id'), date_deleted=None).order_by('name')

    def post(self, request, adopt_id):
        serializer = GenePoolSerializer(
            data=request.data, context={'adopt_id': adopt_id})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        gene_pool = serializer.save(adopt_id=adopt_id)

        return Response(GenePoolSerializer(gene_pool).data, status=status.HTTP_201_CREATED)


class GenePoolApiDetailView(ApiLoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GenePoolSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return GenePool.objects.filter(adopt_id=self.kwargs.get('adopt_id'), date_deleted=None)

    def delete(self, request, pk, **kwargs):
        try:
            gene_pool = self.get_queryset().get(id=pk)
            gene_pool.date_deleted = timezone.now()
            gene_pool.save()

            return Response(status=status.HTTP_202_ACCEPTED)
        except GenePool.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GeneApiView(generics.ListCreateAPIView):
    serializer_class = GeneSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return Gene.objects.filter(gene_pool_id=self.kwargs.get('gene_pool_id'), date_deleted=None).order_by('name')

    def post(self, request, adopt_id, gene_pool_id):
        serializer = GeneSerializer(
            data=request.data, context={'adopt_id': adopt_id})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        adopt = serializer.save(gene_pool_id=gene_pool_id)

        return Response(GeneSerializer(adopt).data, status=status.HTTP_201_CREATED)


class GeneApiDetailView(ApiLoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GeneSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return Gene.objects.filter(gene_pool_id=self.kwargs.get('gene_pool_id'), date_deleted=None)

    def delete(self, request, pk, **kwargs):
        try:
            gene = self.get_queryset().get(id=pk)
            gene.date_deleted = timezone.now()
            gene.save()

            return Response(status=status.HTTP_202_ACCEPTED)
        except Gene.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
