
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
    # (Optional) add when you build it:
    # path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),

    # Tasks (neutral, staff will mostly use these)
    path("tasks/", views.task_list, name="task_list"),
    # If you want a dedicated “new task activity” page for staff:
    path("tasks/select/", views.dashboard_staff, name="task_select"),

    # Reporting
    path("reports/timesheet/", views.timesheet_report, name="timesheet_report"),

    # Integrations (Google Sheets)
    path("integrations/gsheet/transfer-views/", views.get_transfer_views, name="get_transfer_views"),
    path("integrations/gsheet/export/", views.export_to_gsheet, name="export_to_gsheet"),

    # ---- Legacy redirects (keep while users/bookmarks update) ----
    path("select-task/", RedirectView.as_view(pattern_name="timesheet:dashboard_staff", permanent=False)),
    path("staff/select-task/", RedirectView.as_view(pattern_name="timesheet:dashboard_staff", permanent=False)),
]

