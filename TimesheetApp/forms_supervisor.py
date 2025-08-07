from django import forms
from TimesheetApp.models import tblTask, tblTaskLogSupervisor
import datetime
from django.core.exceptions import ValidationError

class TaskSelectionFormSupervisor(forms.Form):
    task = forms.ModelChoiceField(
        queryset=tblTask.objects.all().order_by('task'),
        required=True,
        label="Task",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Date"
    )
    time = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        # widget=forms.Select(attrs={'class': 'form-select'}),
        label="Time"
    )
    work_activities = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Work Activities"
    )
    remarks = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Remarks"
    )

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task'].empty_label = "<Select a task>"
        print("Fields in form:", list(self.fields.keys()))
        if user_id:
            last_task_log = tblTaskLogSupervisor.objects.filter(fk_userid=user_id).order_by('-action_timestamp').first()
            if last_task_log:
                self.fields['task'].queryset = tblTask.objects.exclude(id=last_task_log.fk_taskid.id)
            else:
                self.fields['task'].queryset = tblTask.objects.all()
        else:
            self.fields['task'].queryset = tblTask.objects.all()

    # Ensure that even if the frontend is bypassed, the backend still rejects future timestamps.
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")

        if date and time:
            submitted_dt = datetime.datetime.combine(date, time)
            now = datetime.datetime.now()

            if submitted_dt > now:
                raise ValidationError("You cannot select a future date or time.")

        return cleaned_data

