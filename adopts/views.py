from adopts.serializers import AdoptLayerSerializer, AdoptSerializer, AdoptListSerializer
from adopts.models import Adopt, AdoptLayer
from adopts.permissions import IsAdoptMod
from django.conf import settings
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.response import Response
from users.mixins import ApiLoginRequiredMixin


class AdoptApiView(ApiLoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = AdoptListSerializer

    def get_queryset(self):
        return self.request.user.adopts.filter(date_deleted=None).order_by('name')

    def post(self, request):
        if not settings.RNGADOPTS_ADOPT_CREATION_ENABLED:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = AdoptSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        adopt = serializer.save()
        adopt.mods.add(request.user)

        return Response(AdoptSerializer(adopt).data, status=status.HTTP_201_CREATED)


class AdoptApiDetailView(ApiLoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdoptSerializer

    def get_queryset(self):
        return self.request.user.adopts.filter(date_deleted=None)

    def delete(self, request, pk):
        try:
            adopt = self.get_queryset().get(id=pk)
            adopt.date_deleted = timezone.now()
            adopt.save()

            return Response(status=status.HTTP_202_ACCEPTED)
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

        adopt_layer = serializer.save(adopt_id=adopt_id)

        return Response(AdoptLayerSerializer(adopt_layer).data, status=status.HTTP_201_CREATED)


class AdoptLayerApiDetailView(ApiLoginRequiredMixin, generics.DestroyAPIView, generics.UpdateAPIView):
    serializer_class = AdoptLayerSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return AdoptLayer.objects.filter(adopt_id=self.kwargs.get('adopt_id'))
