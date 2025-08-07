
from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import AuthUser  # your custom tblAuthUser model

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            # Find user in your custom auth table
            auth_user = AuthUser.objects.get(email_address=username)

            # Compare password securely
            if check_password(password, auth_user.password):
                # Create or get a Django User object for session login
                user, _ = User.objects.get_or_create(username=auth_user.email_address)
                return user
        except AuthUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

