from django.urls import path

from users.views import UserApiMeView

app_name = 'users'

urlpatterns = [
    path("me", UserApiMeView.as_view(), name="me"),
]
