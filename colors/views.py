from adopts.models import Adopt
from adopts.permissions import IsAdoptMod
from colors.serializers import ColorPoolSerializer
from colors.models import ColorPool
from colors.actions import create_color_pool, delete_color_pool
from rest_framework import status, generics
from rest_framework.response import Response
from users.mixins import ApiLoginRequiredMixin


class ColorPoolApiView(ApiLoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = ColorPoolSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return ColorPool.objects.active().filter(adopt_id=self.kwargs.get('adopt_id')).order_by('name')

    def post(self, request, adopt_id):
        serializer = ColorPoolSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        color_pool = create_color_pool(
            adopt=Adopt.objects.get(id=adopt_id),
            **serializer.validated_data,
        )

        return Response(ColorPoolSerializer(color_pool).data, status=status.HTTP_201_CREATED)


class ColorPoolApiDetailView(ApiLoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ColorPoolSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return ColorPool.objects.active().filter(adopt_id=self.kwargs.get('adopt_id'))

    def delete(self, request, pk, **kwargs):
        try:
            delete_color_pool(self.get_queryset().get(id=pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ColorPool.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
