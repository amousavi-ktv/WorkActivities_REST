from datetime import datetime, date as date_cls
from django import forms
from django.core.exceptions import ValidationError

from TimesheetApp.models import tblTask, vewUserKey

# ---------- Common small widgets ----------
class SmallText(forms.TextInput):
    def __init__(self, *args, **kwargs):
        attrs = {"class": "form-control form-control-sm"}
        attrs.update(kwargs.pop("attrs", {}))
        super().__init__(attrs=attrs, *args, **kwargs)

class SmallSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        attrs = {"class": "form-select form-select-sm"}
        attrs.update(kwargs.pop("attrs", {}))
        super().__init__(attrs=attrs, *args, **kwargs)

class SmallDate(forms.DateInput):
    input_type = "date"
    def __init__(self, *args, **kwargs):
        attrs = {"class": "form-control form-control-sm", "max": datetime.now().date().isoformat()}
        attrs.update(kwargs.pop("attrs", {}))
        super().__init__(attrs=attrs, *args, **kwargs)

class SmallTime(forms.TimeInput):
    input_type = "time"
    def __init__(self, *args, **kwargs):
        attrs = {"class": "form-control form-control-sm"}
        attrs.update(kwargs.pop("attrs", {}))
        super().__init__(attrs=attrs, *args, **kwargs)

# ---------- STAFF ----------
class TaskSelectionFormStaff(forms.Form):
    task = forms.ModelChoiceField(
        queryset=tblTask.objects.none(),  # set in __init__
        widget=SmallSelect(),
        empty_label="Select task…",
        required=True,
        label="Task",
    )
    work_activities = forms.CharField(
        required=False, widget=SmallText(), label="Work Activities"
    )
    remarks = forms.CharField(
        required=False, widget=SmallText(), label="Remarks"
    )

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Base queryset; view may further trim (exclude last)
        self.fields["task"].queryset = tblTask.objects.all().order_by("task")

# ---------- SUPERVISOR ----------
class TaskSelectionFormSupervisor(forms.Form):
    task = forms.ModelChoiceField(
        queryset=tblTask.objects.none(),
        widget=SmallSelect(),
        empty_label="Select task…",
        required=True,
        label="Task",
    )
    date = forms.DateField(widget=SmallDate(), required=True, label="Activity Date")
    time = forms.TimeField(widget=SmallTime(), required=True, label="Activity Time")
    work_activities = forms.CharField(required=False, widget=SmallText(), label="Work Activities")
    remarks = forms.CharField(required=False, widget=SmallText(), label="Remarks")

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].queryset = tblTask.objects.all().order_by("task")

    def clean(self):
        cleaned = super().clean()
        d = cleaned.get("date")
        t = cleaned.get("time")
        if not d or not t:
            return cleaned

        # No future dates
        today = datetime.now().date()
        if d > today:
            self.add_error("date", "Future dates are not allowed.")
            return cleaned

        # No future time when date == today
        if d == today:
            now_hm = datetime.now().time().replace(second=0, microsecond=0)
            if t > now_hm:
                self.add_error("time", "Future time today is not allowed.")
        return cleaned

# ---------- ADMIN ----------
class AdminTimesheetForm(forms.Form):
    user_key = forms.ModelChoiceField(
        queryset=vewUserKey.objects.none(),
        widget=SmallSelect(),
        empty_label="Select Person (UserKey)…",
        required=True,
        label="Person",
    )
    task = forms.ModelChoiceField(
        queryset=tblTask.objects.none(),
        widget=SmallSelect(),
        empty_label="Select task…",
        required=True,
        label="Activity",
    )
    date = forms.DateField(widget=SmallDate(), required=True, label="Activity Date")
    time = forms.TimeField(widget=SmallTime(), required=True, label="Activity Time")
    work_activities = forms.CharField(required=False, widget=SmallText(), label="Work Activities")
    remarks = forms.CharField(required=False, widget=SmallText(), label="Remarks")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_key"].queryset = vewUserKey.objects.all().order_by("user_key")
        self.fields["task"].queryset = tblTask.objects.all().order_by("task")

    def clean(self):
        cleaned = super().clean()
        d = cleaned.get("date")
        t = cleaned.get("time")
        if not d or not t:
            return cleaned

        today = datetime.now().date()
        if d > today:
            self.add_error("date", "Future dates are not allowed.")
            return cleaned

        if d == today:
            now_hm = datetime.now().time().replace(second=0, microsecond=0)
            if t > now_hm:
                self.add_error("time", "Future time today is not allowed.")
        return cleaned
