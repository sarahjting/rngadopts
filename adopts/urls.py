from django.urls import path

from adopts.views import AdoptApiView, AdoptApiDetailView

app_name = 'adopts'

urlpatterns = [
    path('api/adopts/', AdoptApiView.as_view(), name='api'),
    path('api/adopts/<pk>', AdoptApiDetailView.as_view(), name='api'),
]
