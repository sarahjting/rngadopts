# accounts/views.py
from urllib import request
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserSerializer

from .forms import UserCreationForm


class RegisterView(CreateView):
    """
    This is deprecated now since all our auth is done through Discord, but I guess there's no harm having a password login/register available just in case.
    """
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"


class UserApiMeView(APIView):
    def get(self, request, format=None):
        if not request.user.is_authenticated:
            return Response(None)
        return Response(UserSerializer(request.user).data)
