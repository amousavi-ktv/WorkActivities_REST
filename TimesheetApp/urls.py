# TimesheetApp/urls.py
from django.urls import path
from TimesheetApp import views

app_name = "timesheet"

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/staff/", views.dashboard_staff, name="dashboard_staff"),
    path("dashboard/supervisor/", views.dashboard_supervisor, name="dashboard_supervisor"),
    path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),

    # AJAX endpoints used by Select2
    path("ajax/task-search/", views.task_search, name="task_search"),
    path("ajax/admin-userkey-search/", views.admin_userkey_search, name="admin_userkey_search"),

    # misc/endpoints you already had
    path("task-list/", views.task_list, name="task_list"),
    path("report/", views.timesheet_report, name="timesheet_report"),
    path("export/views/", views.get_transfer_views, name="get_transfer_views"),
    path("export/gsheet/", views.export_to_gsheet, name="export_to_gsheet"),
]
