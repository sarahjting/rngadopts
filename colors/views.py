from adopts.permissions import IsAdoptMod
from colors.serializers import ColorPoolSerializer, ColorPoolListSerializer
from colors.models import ColorPool
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.response import Response
from users.mixins import ApiLoginRequiredMixin


class ColorPoolApiView(ApiLoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = ColorPoolListSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return ColorPool.objects.filter(adopt_id=self.kwargs.get('adopt_id'), date_deleted=None).order_by('name')

    def post(self, request, adopt_id):
        serializer = ColorPoolSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        color_pool = serializer.save(adopt_id=adopt_id)

        return Response(ColorPoolSerializer(color_pool).data, status=status.HTTP_201_CREATED)


class ColorPoolApiDetailView(ApiLoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ColorPoolSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return ColorPool.objects.filter(adopt_id=self.kwargs.get('adopt_id'), date_deleted=None)

    def delete(self, request, pk, **kwargs):
        try:
            color_pool = self.get_queryset().get(id=pk)
            color_pool.date_deleted = timezone.now()
            color_pool.save()

            return Response(status=status.HTTP_202_ACCEPTED)
        except ColorPool.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
