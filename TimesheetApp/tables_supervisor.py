
# TimesheetApp/tables_supervisor.py

import django_tables2 as tables
from TimesheetApp.models import vewTaskLog

class TaskLogSupervisorTable(tables.Table):
    activity_id      = tables.Column(verbose_name="Activity ID")
    user_key         = tables.Column(verbose_name="Person")
    activity_date    = tables.DateColumn(verbose_name="Activity Date", format="d M Y")
    activity_time    = tables.TimeColumn(verbose_name="Activity Time", format="H:i")
    activity         = tables.Column(verbose_name="Activity")
    action_timestamp = tables.DateTimeColumn(verbose_name="Action Time", format="Y-m-d H:i:s")
    admin_id         = tables.Column(verbose_name="Actioned By")
    work_activities  = tables.Column(verbose_name="Work Activities")
    remarks          = tables.Column(verbose_name="Remarks")

    class Meta:
        model = vewTaskLog
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            "activity_id",
            "user_key",
            "activity_date",
            "activity_time",
            "activity",
            "action_timestamp",
            "admin_id",
            "work_activities",
            "remarks",
        )
        attrs = {"class": "table table-striped table-hover table-sm align-middle"}
