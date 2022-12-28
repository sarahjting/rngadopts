from adopts.actions import create_adopt, create_adopt_layer, delete_adopt, delete_adopt_layer
from adopts.serializers import AdoptLayerSerializer, AdoptSerializer, AdoptListSerializer
from adopts.models import Adopt, AdoptLayer
from adopts.permissions import IsAdoptMod
from django.conf import settings
from rest_framework import status, generics
from rest_framework.response import Response
from users.mixins import ApiLoginRequiredMixin


class AdoptApiView(ApiLoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = AdoptListSerializer

    def get_queryset(self):
        return self.request.user.adopts.active().order_by('name')

    def post(self, request):
        if not settings.RNGADOPTS_ADOPT_CREATION_ENABLED:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = AdoptSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        adopt = create_adopt(mod=request.user, **serializer.validated_data,)

        return Response(AdoptSerializer(adopt).data, status=status.HTTP_201_CREATED)


class AdoptApiDetailView(ApiLoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdoptSerializer

    def get_queryset(self):
        return self.request.user.adopts.active()

    def delete(self, request, pk):
        try:
            delete_adopt(self.get_queryset().get(id=pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Adopt.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AdoptLayerApiView(ApiLoginRequiredMixin, generics.CreateAPIView):
    serializer_class = AdoptLayerSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return AdoptLayer.objects.filter(adopt_id=self.kwargs.get('adopt_id')).order_by('-sort')

    def post(self, request, adopt_id):
        serializer = AdoptLayerSerializer(
            data=request.data, context={'adopt_id': adopt_id})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        adopt_layer = create_adopt_layer(
            adopt=Adopt.objects.active().get(id=adopt_id),
            **serializer.validated_data,
        )

        return Response(AdoptLayerSerializer(adopt_layer).data, status=status.HTTP_201_CREATED)


class AdoptLayerApiDetailView(ApiLoginRequiredMixin, generics.DestroyAPIView, generics.UpdateAPIView):
    serializer_class = AdoptLayerSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return AdoptLayer.objects.filter(adopt_id=self.kwargs.get('adopt_id'))

    def delete(self, request, adopt_id, pk):
        try:
            delete_adopt_layer(self.get_queryset().get(id=pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Adopt.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
