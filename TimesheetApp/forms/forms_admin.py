# TimesheetApp/Forms/forms_admin.py
from django import forms
from django.core.exceptions import ValidationError
from TimesheetApp.models import tblAppUser, tblTask, vewUserKey
from TimesheetApp.models import tblTaskLogAdmin, tblTask, vewUserKey

class AdminTimesheetForm(forms.Form):
    user_key = forms.ModelChoiceField(
        queryset=vewUserKey.objects.all().order_by('user_key'),
        label="Employee",
        required=True,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    class Meta:
            model = tblTaskLogAdmin
            fields = ['user_key', 'task', 'date', 'time', 'work_activities', 'remarks']
            widgets = {
                'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
                'work_activities': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
                'remarks': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
                'task': forms.Select(attrs={'class': 'form-select'}),
            }

    task = forms.ModelChoiceField(
        label="Task",
        queryset=tblTask.objects.all().order_by("task"),
        required=True,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    date = forms.DateField(
        label="Date",
        required=True,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    time = forms.TimeField(
        label="Time",
        required=True,
        widget=forms.TimeInput(attrs={"type": "time", "class": "form-control"})
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

    def clean_pid(self):
        pid = self.cleaned_data["pid"].strip().upper()
        if not tblAppUser.objects.filter(pid=pid, is_active=True).exists():
            raise ValidationError("No active user found with this PID.")
        return pid

    def get_user(self):
        return tblAppUser.objects.get(pid=self.cleaned_data["pid"].strip().upper(), is_active=True)

