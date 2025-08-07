
from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect

def require_staff_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request, 'auth_user') or request.auth_user is None:
            return HttpResponseForbidden("Access denied.")
        if not request.auth_user.is_staff:
            return HttpResponseForbidden("You do not have permission to access this area.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def require_auth_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request, 'auth_user') or request.auth_user is None:
            return redirect('login')  # Named URL to your welcome/login page
        return view_func(request, *args, **kwargs)
    return _wrapped_view