from django.urls import path

from users.views import RegisterView

app_name = 'auth'

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
]
