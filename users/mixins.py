from django.contrib.auth.mixins import LoginRequiredMixin


class ApiLoginRequiredMixin(LoginRequiredMixin):
    raise_exception = True
