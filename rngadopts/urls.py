"""rngadopts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path('', include('frontend.urls')),
    path('auth/', include('users.urls.auth')),
    path('auth/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),

    # 4 arguments: route pattern, view, kwargs, name
    path('admin/', admin.site.urls),

    path('', include('colors.urls', namespace='colors')),
    path('', include('adopts.urls', namespace='adopts')),
    path('', include('users.urls.users', namespace='users')),
    path('', include('genes.urls', namespace='genes')),

    # this catches everything else and shoots it to the spa
    re_path(r'^.*', include('frontend.urls')),
]
