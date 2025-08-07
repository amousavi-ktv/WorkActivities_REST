import django_tables2 as tables
from TimesheetApp.models import vewTaskLogStaff

class TaskLogStaffTable(tables.Table):
    date = tables.DateColumn(format="d M Y")  # ISO date
    time = tables.TimeColumn(format="H:i")    # ISO time
    action_timestamp = tables.DateTimeColumn(format="Y-m-d H:i:s")  # Full ISO datetime
    class Meta:
        model = vewTaskLogStaff
        template_name = "django_tables2/bootstrap4.html"
        fields = ("activity_timestamp", "task", "task_key", "work_activities", "remarks")


