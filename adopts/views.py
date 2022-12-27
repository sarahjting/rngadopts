from adopts.serializers import AdoptSerializer
from adopts.models import Adopt
from django.conf import settings
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.response import Response
from users.mixins import ApiLoginRequiredMixin


class AdoptApiView(ApiLoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = AdoptSerializer

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


class AdoptApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdoptSerializer

    def get_queryset(self):
        return self.request.user.adopts.filter(date_deleted=None)

    def delete(self, request, pk):
        try:
            adopt = self.get_queryset().get(id=pk)
            adopt.date_deleted = timezone.now()
            adopt.save()

            return Response(AdoptSerializer(adopt).data, status=status.HTTP_202_ACCEPTED)
        except Adopt.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
