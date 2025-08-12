"""
Definition of urls for WorkActivities/url.py.
"""
# urls.py
# WorkActivities/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # App routes
    path("", include("TimesheetApp.urls", namespace="timesheet")),  # <-- IMPORTANT

    # Social auth
    path("auth/", include("social_django.urls", namespace="social")),

    # API v1 (your existing DRF routes)
    path("api/v1/", include("TimesheetApp.api_urls")),  # you can later add v2 side-by-side
]
