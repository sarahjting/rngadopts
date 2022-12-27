from adopts.permissions import IsAdoptMod
from colors.serializers import ColorPoolSerializer
from colors.models import ColorPool
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.response import Response
from users.mixins import ApiLoginRequiredMixin


class ColorPoolApiView(generics.ListCreateAPIView):
    serializer_class = ColorPoolSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return self.request.user.adopts.get(id=self.kwargs['adopt_id']).color_pools.filter(date_deleted=None).order_by('name')

    def post(self, request, adopt_id):
        serializer = ColorPoolSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        adopt = serializer.save(adopt_id=adopt_id)

        return Response(ColorPoolSerializer(adopt).data, status=status.HTTP_201_CREATED)


class ColorPoolApiDetailView(ApiLoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ColorPoolSerializer
    permission_classes = [IsAdoptMod]

    def get_queryset(self):
        return self.request.user.adopts.get(id=self.kwargs['adopt_id']).color_pools.filter(date_deleted=None)

    def delete(self, request, pk, **kwargs):
        try:
            color_pool = self.get_queryset().get(id=pk)
            color_pool.date_deleted = timezone.now()
            color_pool.save()

            return Response(ColorPoolSerializer(color_pool).data, status=status.HTTP_202_ACCEPTED)
        except ColorPool.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
