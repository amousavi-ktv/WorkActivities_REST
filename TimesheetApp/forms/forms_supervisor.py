# TimesheetApp/forms/forms_supervisor.py

from django import forms
from TimesheetApp.models import tblTask


class TaskSelectionFormSupervisor(forms.Form):
    """
    Supervisor timesheet entry form.
    - Uses Select2 AJAX for the `task` field, so the queryset starts empty.
    - Accepts `user_id` in __init__ to match the existing views.py call signature.
      (We don't currently use user_id for filtering, but we accept it to avoid errors.)
    """

    task = forms.ModelChoiceField(
        label="Task",
        queryset=tblTask.objects.none(),  # AJAX: start empty
        required=True,
        widget=forms.Select(attrs={"class": "form-select", "id": "id_task"}),
    )

    date = forms.DateField(
        label="Date",
        required=True,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control", "id": "id_date"}),
    )

    time = forms.TimeField(
        label="Time",
        required=True,
        widget=forms.TimeInput(attrs={"type": "time", "class": "form-control", "id": "id_time"}),
    )

    work_activities = forms.CharField(
        label="Work activities",
        required=False,
        widget=forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
    )

    remarks = forms.CharField(
        label="Remarks",
        required=False,
        widget=forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
    )

    def __init__(self, *args, user_id=None, **kwargs):
        """
        Accept `user_id` so the view can call:
            TaskSelectionFormSupervisor(request.POST, user_id=auth_user_id)
        We keep it optional and unused for now (but you can use it later to filter tasks).
        """
        super().__init__(*args, **kwargs)

        # Allow validation of the selected task on POST (Select2 sends the pk).
        sel_task = self.data.get("task")
        if sel_task:
            self.fields["task"].queryset = tblTask.objects.filter(pk=sel_task)
        else:
            self.fields["task"].queryset = tblTask.objects.none()
