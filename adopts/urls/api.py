from django.urls import path

from adopts.views import AdoptApiView, AdoptApiDetailView

app_name = 'adopts'

urlpatterns = [
    path('', AdoptApiView.as_view(), name='api'),
    path('<pk>', AdoptApiDetailView.as_view(), name='api'),
]
