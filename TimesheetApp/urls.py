# TimesheetApp/urls.py
from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "timesheet"

urlpatterns = [
    # Entry & auth
    path("", views.welcome, name="welcome"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboards
    path("dashboard/", views.dashboard, name="dashboard"),  # role-aware
    path("dashboard/staff/", views.dashboard_staff, name="dashboard_staff"),
    path("dashboard/supervisor/", views.dashboard_supervisor, name="dashboard_supervisor"),
    path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),

    # Tasks (neutral)
    path("tasks/", views.task_list, name="task_list"),

    # Reporting
    path("reports/timesheet/", views.timesheet_report, name="timesheet_report"),

    # Integrations (Google Sheets)
    path("integrations/gsheet/transfer-views/", views.get_transfer_views, name="get_transfer_views"),
    path("integrations/gsheet/export/", views.export_to_gsheet, name="export_to_gsheet"),

    # AJAX search endpoints for Select2
    path("search/tasks/", views.task_search, name="task_search"),
    path("admin/search/user-keys/", views.admin_userkey_search, name="admin_userkey_search"),

    # Legacy redirects (optional)
    path("select-task/", RedirectView.as_view(pattern_name="timesheet:dashboard_staff", permanent=False)),
    path("staff/select-task/", RedirectView.as_view(pattern_name="timesheet:dashboard_staff", permanent=False)),
]
