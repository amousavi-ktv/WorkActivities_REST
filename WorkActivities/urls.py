"""
Definition of urls for WorkActivities/url.py.
"""
# urls.py
# WorkActivities/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # App routes
    path("", include("TimesheetApp.urls", namespace="timesheet")),  # <-- IMPORTANT

    # Social auth
    path("auth/", include("social_django.urls", namespace="social")),

    # API v1 (your existing DRF routes)
    path("api/v1/", include("TimesheetApp.api_urls")),  # you can later add v2 side-by-side

    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
]
