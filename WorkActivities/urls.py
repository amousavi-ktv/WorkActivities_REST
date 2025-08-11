"""
Definition of urls for WorkActivities.
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

# """
# Definition of urls for WorkActivities.
# """
# # urls.py
# from django.contrib import admin
# from django.urls import path, include
# from TimesheetApp import views
# from TimesheetApp.views import dashboard
# from TimesheetApp.views import logout_view
# from TimesheetApp import views
# from django.contrib.auth.views import LogoutView
# # from . import views

# urlpatterns = [
#     path('', views.welcome, name='login'),  # ?? so 'login' exists!
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('select-task/', views.dashboard_staff, name='dashboard_staff'),
#     path('task-list/', views.task_list, name='task_list'),
#     path('admin/', admin.site.urls),
#     path('auth/', include('social_django.urls', namespace='social')),
#     path('staff/select-task/', views.dashboard_staff, name='dashboard_staff'),
#     path('api/', include('TimesheetApp.api_urls')),     # for REST
#     path('timesheet-report/', views.timesheet_report, name='timesheet_report'),
#     path('api/transfer-views/', views.get_transfer_views, name='get_transfer_views'),
#     path('api/export-to-gsheet/', views.export_to_gsheet, name='export_to_gsheet'),
# ]