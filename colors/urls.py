from django.urls import path
from colors.views import ColorPoolApiView, ColorPoolApiDetailView

app_name = 'colors'

urlpatterns = [
    path('api/adopts/<adopt_id>/color-pools',
         ColorPoolApiView.as_view(), name='api'),
    path('api/adopts/<adopt_id>/color-pools/<pk>',
         ColorPoolApiDetailView.as_view(), name='api'),
]
