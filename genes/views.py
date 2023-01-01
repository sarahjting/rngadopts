from adopts.models import Adopt
from adopts.permissions import IsAdoptMod
from genes.actions import create_gene, create_gene_layer, create_gene_pool, delete_gene, delete_gene_pool, update_gene
from genes.serializers import GeneLayerSerializer, GenePoolSerializer, GenePoolListSerializer, GeneSerializer, GeneListSerializer
from genes.models import GeneLayer, GenePool, Gene
from rest_framework import status, generics
from rest_framework.response import Response
from users.mixins import ApiLoginRequiredMixin
from django.db.models import Prefetch


class GenePoolApiView(ApiLoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = GenePoolListSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return (GenePool.objects.active().filter(adopt_id=self.kwargs.get("adopt_id"))
                .prefetch_related("color_pool")
                .prefetch_related(Prefetch("genes", queryset=Gene.objects.active().order_by("name"),))
                .prefetch_related("genes__color_pool")
                .order_by("name"))

    def post(self, request, adopt_id):
        serializer = GenePoolSerializer(
            data=request.data, context={'adopt_id': adopt_id})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        gene_pool = create_gene_pool(
            adopt=Adopt.objects.get(id=adopt_id),
            **serializer.validated_data,
        )

        return Response(GenePoolSerializer(gene_pool).data, status=status.HTTP_201_CREATED)


class GenePoolApiDetailView(ApiLoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GenePoolSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return GenePool.objects.active().filter(adopt_id=self.kwargs.get('adopt_id'))

    def delete(self, request, adopt_id, pk):
        try:
            delete_gene_pool(self.get_queryset().get(id=pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except GenePool.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GeneApiView(ApiLoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = GeneListSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return Gene.objects.active().filter(gene_pool_id=self.kwargs.get('gene_pool_id')).order_by('name')

    def post(self, request, adopt_id, gene_pool_id):
        serializer = GeneSerializer(
            data=request.data, context={'adopt_id': adopt_id})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        gene = create_gene(
            adopt=Adopt.objects.get(id=adopt_id),
            gene_pool=GenePool.objects.get(id=gene_pool_id),
            **serializer.validated_data,
        )

        return Response(GeneSerializer(gene).data, status=status.HTTP_201_CREATED)


class GeneApiDetailView(ApiLoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GeneSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return Gene.objects.active().filter(gene_pool_id=self.kwargs.get('gene_pool_id'))

    def update(self, request, adopt_id, gene_pool_id, pk):
        try:
            gene = self.get_queryset().get(id=pk)
            serializer = GeneSerializer(gene,
                                        data=request.data, context={'adopt_id': adopt_id})

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            update_gene(gene=gene, **serializer.validated_data)

            return Response(GeneSerializer(gene).data, status=status.HTTP_200_OK)
        except Gene.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, **kwargs):
        try:
            delete_gene(self.get_queryset().get(id=pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Gene.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GeneLayerApiView(ApiLoginRequiredMixin, generics.CreateAPIView):
    serializer_class = GeneLayerSerializer
    permission_classes = [IsAdoptMod]

    def post(self, request, adopt_id):
        serializer = GeneLayerSerializer(
            data=request.data, context={'adopt_id': adopt_id})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        gene_layer = create_gene_layer(
            adopt=Adopt.objects.get(id=adopt_id),
            **serializer.validated_data,
        )

        return Response(GeneLayerSerializer(gene_layer).data, status=status.HTTP_201_CREATED)


class GeneLayerApiDetailView(ApiLoginRequiredMixin, generics.DestroyAPIView, generics.UpdateAPIView):
    serializer_class = GeneLayerSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return GeneLayer.objects.filter(gene__gene_pool__adopt_id=self.kwargs.get('adopt_id'))
