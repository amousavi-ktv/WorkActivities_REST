

# TimesheetApp/backends.py
from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import tblAuthUser  # <-- fix this

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            auth_user = tblAuthUser.objects.get(email_address=username)
            if check_password(password, auth_user.password):
                user, _ = User.objects.get_or_create(username=auth_user.email_address)
                return user
        except tblAuthUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

