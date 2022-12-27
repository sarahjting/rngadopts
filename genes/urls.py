from django.urls import path
from genes.views import GenePoolApiView, GenePoolApiDetailView, GeneApiView, GeneApiDetailView

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
]
