from django import forms
from TimesheetApp.models import tblTask, tblTaskLogStaff

class TaskSelectionFormStaff(forms.Form):
    task = forms.ModelChoiceField(
        queryset=tblTask.objects.all().order_by('task'),
        required=True,
        label="Task",
        widget=forms.Select(attrs={'class': 'form-select'})
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
            last_task_log = tblTaskLogStaff.objects.filter(fk_userid=user_id).order_by('-activity_timestamp').first()
            if last_task_log:
                self.fields['task'].queryset = tblTask.objects.exclude(id=last_task_log.fk_taskid.id)
            else:
                self.fields['task'].queryset = tblTask.objects.all()
        else:
            self.fields['task'].queryset = tblTask.objects.all()

# from django import forms
# from TimesheetApp.models import tblTask, vewTaskLogStaff

# class TaskSelectionFormStaff(forms.Form):
#     task = forms.ModelChoiceField(queryset=tblTask.objects.none())

    # def __init__(self, *args, user_id=None, **kwargs):
    #     super().__init__(*args, **kwargs)
        
    #     # now this works because TaskLogStaff is properly imported
    #     last_task = vewTaskLogStaff.objects.filter(fk_userid=user_id).order_by('-activity_timestamp').first()
        
    #     if last_task:
    #         self.fields['task'].queryset = tblTask.objects.exclude(id=last_task.fk_taskid)
    #     else:
    #         self.fields['task'].queryset = tblTask.objects.all()

