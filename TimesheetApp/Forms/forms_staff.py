#
# TimesheetApp/Forms/forms_staff.py
#
from django import forms
from TimesheetApp.models import tblTask

class TaskSelectionFormStaff(forms.Form):
    task = forms.ModelChoiceField(
        label="Task",
        queryset=tblTask.objects.none(),              # AJAX: start empty
        required=True,
        widget=forms.Select(attrs={"class": "form-select", "id": "id_task"})
    )
    work_activities = forms.CharField(
        label="Work Activities",
        required=False,
        widget=forms.Textarea(attrs={"rows": 2, "class": "form-control"})
    )
    remarks = forms.CharField(
        label="Remarks",
        required=False,
        widget=forms.Textarea(attrs={"rows": 2, "class": "form-control"})
    )

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        task_id = self.data.get("task")
        if task_id:
            self.fields["task"].queryset = tblTask.objects.filter(pk=task_id)
        else:
            self.fields["task"].queryset = tblTask.objects.none()
