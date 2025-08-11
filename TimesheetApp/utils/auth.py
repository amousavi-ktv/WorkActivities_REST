# utils/auth.py
from functools import wraps
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from myapp.models import tblRole  # change 'myapp' to your app label

def _get_user_role_key(user):
    """
    Get RoleKey from tblRole via fk_roleID.
    Uses the related object if loaded, otherwise fetches by ID.
    """
    # If we already have the related role object
    if getattr(user, "fk_roleID", None) and hasattr(user.fk_roleID, "role_key"):
        return user.fk_roleID.role_key

    # Fallback to the raw FK id
    if getattr(user, "fk_roleID_id", None):
        try:
            return tblRole.objects.only("role_key").get(pk=user.fk_roleID_id).role_key
        except tblRole.DoesNotExist:
            return None

    return None


def require_roles(*allowed_role_keys, redirect_name=None):
    """
    Restrict access to users whose tblRole.RoleKey is in allowed_role_keys.
    Example:
        @require_roles("SUPERADMIN", "ADMIN")
    """
    allowed = {key.upper() for key in allowed_role_keys}

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")  # change to your login URL name

            user_key = _get_user_role_key(request.user)
            if not user_key or user_key.upper() not in allowed:
                if redirect_name:
                    return redirect(redirect_name)
                raise PermissionDenied("You do not have permission to view this page.")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
