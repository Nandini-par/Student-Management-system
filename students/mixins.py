
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

class StaffRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("Staff access only")
        return super().dispatch(request, *args, **kwargs)


class AdminOnlyMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Admin access only")
        return super().dispatch(request, *args, **kwargs)


class ReadOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.method != 'GET':
            return HttpResponseForbidden("Read-only access")
        return super().dispatch(request, *args, **kwargs)
