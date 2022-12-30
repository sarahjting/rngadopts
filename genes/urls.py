from django.urls import path
from genes.views import GenePoolApiView, GenePoolApiDetailView, GeneApiView, GeneApiDetailView, GeneLayerApiView, GeneLayerApiDetailView
from django.conf import settings
from django.conf.urls.static import static


app_name = 'genes'

urlpatterns = [
    path('api/adopts/<adopt_id>/gene-pools',
         GenePoolApiView.as_view(), name='pool_api'),
    path('api/adopts/<adopt_id>/gene-pools/<pk>',
         GenePoolApiDetailView.as_view(), name='pool_api'),
    path('api/adopts/<adopt_id>/gene-pools/<gene_pool_id>/genes',
         GeneApiView.as_view(), name='api'),
    path('api/adopts/<adopt_id>/gene-pools/<gene_pool_id>/genes/<pk>',
         GeneApiDetailView.as_view(), name='api'),
    path('api/adopts/<adopt_id>/gene-layers',
         GeneLayerApiView.as_view(), name='layers_api'),
    path('api/adopts/<adopt_id>/gene-layers/<pk>',
         GeneLayerApiDetailView.as_view(), name='layers_api'),
]

# serve static files from dev server; in prod use a proper webserver
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
