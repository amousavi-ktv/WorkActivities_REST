# TimesheetApp/Forms/forms_admin.py
from django import forms
from TimesheetApp.models import tblAppUser, tblTask, vewUserKey

class AdminTimesheetForm(forms.Form):
    user_key = forms.ModelChoiceField(
        label="Employee",
        queryset=vewUserKey.objects.none(),           # AJAX: start empty
        required=True,
        widget=forms.Select(attrs={"class": "form-select", "id": "id_user_key"})
    )
    task = forms.ModelChoiceField(
        label="Task",
        queryset=tblTask.objects.none(),              # AJAX: start empty
        required=True,
        widget=forms.Select(attrs={"class": "form-select", "id": "id_task"})
    )
    date = forms.DateField(
        label="Date",
        required=True,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control", "id": "id_date"})
    )
    time = forms.TimeField(
        label="Time",
        required=True,
        widget=forms.TimeInput(attrs={"type": "time", "class": "form-control", "id": "id_time"})
    )
    work_activities = forms.CharField(
        label="Work activities",
        required=False,
        widget=forms.Textarea(attrs={"rows": 2, "class": "form-control"})
    )
    remarks = forms.CharField(
        label="Remarks",
        required=False,
        widget=forms.Textarea(attrs={"rows": 2, "class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        """
        Keep dropdowns empty for Select2 AJAX. On POST, allow the chosen values to validate
        by narrowing the queryset to the posted ids.
        """
        super().__init__(*args, **kwargs)

        sel_user_key = self.data.get("user_key")
        if sel_user_key:
            self.fields["user_key"].queryset = vewUserKey.objects.filter(user_key=sel_user_key)
        else:
            self.fields["user_key"].queryset = vewUserKey.objects.none()

        sel_task = self.data.get("task")
        if sel_task:
            self.fields["task"].queryset = tblTask.objects.filter(pk=sel_task)
        else:
            self.fields["task"].queryset = tblTask.objects.none()

    def get_user(self):
        """Map the chosen vewUserKey to the actual tblAppUser object."""
        vk = self.cleaned_data["user_key"]  # instance of vewUserKey
        return tblAppUser.objects.get(user_key=vk.user_key, is_active=True)
