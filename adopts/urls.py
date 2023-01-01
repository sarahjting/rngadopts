from django.urls import path
from adopts.views import AdoptApiView, AdoptApiDetailView, AdoptLayerApiView, AdoptLayerApiDetailView, AdoptGenView, AdoptGenApiView

app_name = 'adopts'

urlpatterns = [
    path('gen/<file_name>.png', AdoptGenView.as_view(), name='gen'),
    path('api/adopt-gen/<pk>', AdoptGenApiView.as_view(), name='api_gen'),
    path('api/adopts/', AdoptApiView.as_view(), name='api'),
    path('api/adopts/<pk>', AdoptApiDetailView.as_view(), name='api'),
    path('api/adopts/<adopt_id>/layers',
         AdoptLayerApiView.as_view(), name='layers_api'),
    path('api/adopts/<adopt_id>/layers/<pk>',
         AdoptLayerApiDetailView.as_view(), name='layers_api'),
]
