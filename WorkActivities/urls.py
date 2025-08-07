"""
Definition of urls for WorkActivities.
"""
# urls.py
from django.contrib import admin
from django.urls import path, include
from TimesheetApp import views
from TimesheetApp.views import dashboard
from TimesheetApp.views import logout_view
from TimesheetApp import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.welcome, name='login'),  # ?? so 'login' exists!
    path('dashboard/', views.dashboard, name='dashboard'),
    path('select-task/', views.task_selection_staff, name='task_selection_staff'),
    path('task-list/', views.task_list, name='task_list'),
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('staff/select-task/', views.task_selection_staff, name='task_selection_staff'),
    path('api/', include('TimesheetApp.api_urls')),     # for REST
    path('timesheet-report/', views.timesheet_report, name='timesheet_report'),
]