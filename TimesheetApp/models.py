
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

# This file was created by running the following command:

# E:\AppServer\Applications\WorkActivities> .\env\Scripts\activate.ps1

# (env) PS E:\AppServer\Applications\WorkActivities> python manage.py inspectdb > main_models.txt
# (env) PS E:\AppServer\Applications\WorkActivities> python manage.py inspectdb tblSample > sample_model.txt

# models.py
from django.db import models

class tblTask(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    task_key = models.CharField(db_column='TaskKey', unique=True, max_length=40, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    task = models.CharField(db_column='Task', unique=True, max_length=40, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=250, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False  # Don't let Django manage this table (no CREATE/DROP)
        db_table = 'tblTask'  # Match your exact SQL Server table name
    def __str__(self):
        return self.task

class tblRole(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    role_key = models.CharField(db_column='RoleKey', max_length=20, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    role = models.CharField(db_column='RoleName', max_length=40, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=250, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'tblRole'

class tblAppUser(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pid = models.CharField(db_column='PID', unique=True, max_length=4, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    user_key = models.CharField(db_column='UserKey', unique=True, max_length=12, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    firstame = models.CharField(db_column='Firstame', max_length=50, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    surname = models.CharField(db_column='Surname', max_length=50, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    fk_roleid = models.ForeignKey(tblRole, models.DO_NOTHING, db_column='fk_RoleID', blank=True, null=True)  # Field name made lowercase.
    is_active = models.BooleanField(db_column='IsActive')  # Field name made lowercase.
    email_address = models.CharField(db_column='EmailAddress', max_length=50, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'tblUser'
    def __str__(self):
        return self.pid  # or return f"{self.firstname} {self.surname}" if preferred

class tblAuthUser(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    fk_userid = models.ForeignKey(tblAppUser, db_column='fk_UserID', on_delete=models.DO_NOTHING)
    auth_provider = models.CharField(db_column='AuthProvider', max_length=20, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    email_address = models.CharField(db_column='ProviderUserID', max_length=255, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=128, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.
    last_login_at = models.DateTimeField(db_column='LastLoginAt', blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=10, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'tblAuthUser'
        
class tblTaskLogAdmin(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    fk_userid = models.ForeignKey(tblAppUser, models.DO_NOTHING, db_column='fk_UserID', related_name='tasklogadmin_user', blank=True, null=True)  # Field name made lowercase.
    fk_taskid = models.ForeignKey(tblTask, models.DO_NOTHING, db_column='fk_TaskID', related_name='tasklogadmin_task', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    time = models.TimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    action_timestamp = models.DateTimeField(db_column='ActionTimestamp', blank=True, null=True)  # Field name made lowercase.
    work_activities = models.CharField(db_column='WorkActivities', max_length=250, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fk_operatorid = models.ForeignKey(tblAppUser, models.DO_NOTHING, db_column='fk_OperatorID', related_name='tbltasklogadmin_fk_operatorid_set', blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=250, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'tblTaskLog_Admin'
        unique_together = (('fk_userid', 'fk_taskid', 'date', 'time'),)

class tblTaskLogSupervisor(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    fk_userid = models.ForeignKey(tblAppUser, models.DO_NOTHING, db_column='fk_UserID', related_name='tasklogsupervisor_user')  # Field name made lowercase.
    fk_taskid = models.ForeignKey(tblTask, models.DO_NOTHING, db_column='fk_TaskID', related_name='tasklogsupervisor_task')  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    time = models.TimeField(db_column='Time')  # Field name made lowercase.
    action_timestamp = models.DateTimeField(db_column='ActionTimestamp')  # Field name made lowercase.
    work_activities = models.CharField(db_column='WorkActivities', max_length=250, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=250, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'tblTaskLog_Supervisor'
        unique_together = (('fk_userid', 'fk_taskid', 'date', 'time'),)

class tblTaskLogStaff(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    fk_userid = models.ForeignKey(tblAppUser, models.DO_NOTHING, db_column='fk_UserID', related_name='tasklogstaff_user')  # Field name made lowercase.
    fk_taskid = models.ForeignKey(tblTask, models.DO_NOTHING, db_column='fk_TaskID', related_name='tasklogstaff_task')  # Field name made lowercase.
    activity_timestamp = models.DateTimeField(db_column='ActivityTimestamp')  # Field name made lowercase.
    work_activities = models.CharField(db_column='WorkActivities', max_length=250, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=250, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'tblTaskLog_Staff' 
        unique_together = (('fk_userid', 'fk_taskid', 'activity_timestamp'),)

class vewTaskLogAdmin(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)   # done manually
    user_key = models.CharField(db_column='UserKey', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='PID', max_length=4, blank=True, null=True)  # Field name made lowercase.
    task = models.CharField(db_column='Task', max_length=40, blank=True, null=True)  # Field name made lowercase.
    task_key = models.CharField(db_column='TaskKey', max_length=40, blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(db_column='RoleName', max_length=40, blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    time = models.TimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    action_timestamp = models.DateTimeField(db_column='ActionTimestamp', blank=True, null=True)  # Field name made lowercase.
    activity_timestamp = models.DateTimeField(db_column='ActivityTimestamp', blank=True, null=True)  # Field name made lowercase.
    fk_taskid = models.IntegerField(db_column='fk_TaskID', blank=True, null=True)  # Field name made lowercase.
    fk_userid = models.IntegerField(db_column='fk_UserID', blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=4, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'vewTaskLog_Admin'

class vewTaskLogSupervisor(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # done manually
    user_key = models.CharField(db_column='UserKey', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='PID', max_length=4, blank=True, null=True)  # Field name made lowercase.
    task = models.CharField(db_column='Task', max_length=40, blank=True, null=True)  # Field name made lowercase.
    task_key = models.CharField(db_column='TaskKey', max_length=40, blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(db_column='RoleName', max_length=40, blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    time = models.TimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    action_timestamp = models.DateTimeField(db_column='ActionTimestamp', blank=True, null=True)  # Field name made lowercase.
    activity_timestamp = models.DateTimeField(db_column='ActivityTimestamp', blank=True, null=True)  # Field name made lowercase.
    fk_taskid = models.IntegerField(db_column='fk_TaskID', blank=True, null=True)  # Field name made lowercase.
    fk_userid = models.IntegerField(db_column='fk_UserID', blank=True, null=True)  # Field name made lowercase.
    work_activities = models.CharField(db_column='WorkActivities', max_length=250, blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=250, blank=True, null=True)  # Field name made lowercase.
    task_logid = models.IntegerField(db_column='TaskLogID')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'vewTaskLog_Supervisor'
        
class vewTaskLogStaff(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # done manually
    user_key = models.CharField(db_column='UserKey', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='PID', max_length=4, blank=True, null=True)  # Field name made lowercase.
    task = models.CharField(db_column='Task', max_length=40, blank=True, null=True)  # Field name made lowercase.
    task_key = models.CharField(db_column='TaskKey', max_length=40, blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(db_column='RoleName', max_length=40, blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    time = models.TimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    action_timestamp = models.DateTimeField(db_column='ActionTimestamp')  # Field name made lowercase.
    fk_taskid = models.IntegerField(db_column='fk_TaskID')  # Field name made lowercase.
    fk_userid = models.IntegerField(db_column='fk_UserID')  # Field name made lowercase.
    work_activities = models.CharField(db_column='WorkActivities', max_length=250, blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=250, blank=True, null=True)  # Field name made lowercase.
    task_logid = models.IntegerField(db_column='TaskLogID')  # Field name made lowercase.
    activity_timestamp = models.DateTimeField(db_column='ActivityTimestamp')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'vewTaskLog_Staff'

class tblSettings(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parameterkey = models.CharField(db_column='ParameterKey', max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    parameter = models.CharField(db_column='Parameter', max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    value = models.TimeField(db_column='Value', blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=150, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'tblSetting'

class vewUserDetails(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    pid = models.CharField(db_column='PID', max_length=4)  # Field name made lowercase.
    user_key = models.CharField(db_column='UserKey', max_length=12)  # Field name made lowercase.
    firstame = models.CharField(db_column='Firstame', max_length=50)  # Field name made lowercase.
    surname = models.CharField(db_column='Surname', max_length=50)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_roleid = models.IntegerField(db_column='fk_RoleID', blank=True, null=True)  # Field name made lowercase.
    is_active = models.BooleanField(db_column='IsActive', blank=True, null=True)  # Field name made lowercase.
    role_key = models.CharField(db_column='RoleKey', max_length=20, blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(db_column='RoleName', max_length=40, blank=True, null=True)  # Field name made lowercase.
    role_remarks = models.CharField(db_column='RoleRemarks', max_length=250, blank=True, null=True)  # Field name made lowercase.
    email_address = models.CharField(db_column='EmailAddress', max_length=50, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'vewUserDetails'

class vewActivitiesTimesheetFullRange_GSheet(models.Model):
    view_index = models.BigIntegerField(db_column='ViewIndex', primary_key=True)  # Field name made lowercase.
    error_message = models.CharField(db_column='ErrorMessage', max_length=250, blank=True, null=True)  # Field name made lowercase.
    employee_id = models.CharField(db_column='Employee_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    lunch_break_hours_field = models.DecimalField(db_column='Lunch Break (Hours)', max_digits=7, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    break_outside_lunchtime_hours_field = models.DecimalField(db_column='Break Outside Lunchtime (Hours)', max_digits=7, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    worked_hours_field = models.DecimalField(db_column='Worked (Hours)', max_digits=7, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    work_target_hours_field = models.DecimalField(db_column='Work Target (Hours)', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    net_balance = models.DecimalField(db_column='NetBalance', max_digits=21, decimal_places=13, blank=True, null=True)  # Field name made lowercase.
    activity_date = models.DateField(db_column='ActivityDate', blank=True, null=True)  # Field name made lowercase.
    daily_target_duration = models.CharField(db_column='DailyTargetDuration', max_length=513, blank=True, null=True)  # Field name made lowercase.
    daily_target_duration_brief_field = models.CharField(db_column='Daily Target Duration (Brief)', max_length=513, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    daily_status = models.CharField(db_column='DailyStatus', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    absence_code = models.CharField(db_column='AbsenceCode', max_length=4000)  # Field name made lowercase.
    work_start_time = models.DateTimeField(db_column='WorkStartTime', blank=True, null=True)  # Field name made lowercase.
    work_end_time = models.DateTimeField(db_column='WorkEndTime', blank=True, null=True)  # Field name made lowercase.
    lunchbreak_start_time = models.DateTimeField(db_column='LunchBreakStartTime', blank=True, null=True)  # Field name made lowercase.
    lunchbreak_end_time = models.DateTimeField(db_column='LunchBreakEndTime', blank=True, null=True)  # Field name made lowercase.
    late_attendance = models.DecimalField(db_column='LateAttendance', max_digits=12, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    early_leave = models.DecimalField(db_column='EarlyLeave', max_digits=12, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    employee_index = models.BigIntegerField(db_column='EmployeeIndex', blank=True, null=True)  # Field name made lowercase.
    adjusted_hijri_month = models.IntegerField(db_column='AdjustedHijriMonth', blank=True, null=True)  # Field name made lowercase.
    adjusted_hijri_day = models.IntegerField(db_column='AdjustedHijriDay', blank=True, null=True)  # Field name made lowercase.
    adjusted_daily_target = models.DecimalField(db_column='Adjusted Daily Target', max_digits=15, decimal_places=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    adjusted_net_balance_hours_field = models.DecimalField(db_column='Adjusted Net Balance (Hours)', max_digits=25, decimal_places=13, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    class Meta:
        managed = False
        db_table = 'vewActivitiesTimesheetFullRange_GSheet'

class vewActivitiesAbsenceRecord_GSheet(models.Model):
    view_index = models.BigIntegerField(db_column='ViewIndex', primary_key=True)  # Field name made lowercase.
    employee_id = models.CharField(db_column='Employee_ID', max_length=5, blank=True, null=True)  # Field name made lowercase.
    activity_date = models.DateField(db_column='ActivityDate', blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='Timestamp', blank=True, null=True)  # Field name made lowercase.
    absence_code = models.CharField(db_column='AbsenceCode', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    request_optioncode = models.CharField(db_column='RequestOptionCode', max_length=2, blank=True, null=True)  # Field name made lowercase.
    approval_status = models.CharField(db_column='ApprovalStatus', max_length=50, blank=True, null=True)  # Field name made lowercase.
    requestor_id = models.CharField(db_column='Requestor_ID', max_length=5, blank=True, null=True)  # Field name made lowercase.
    date_from = models.DateTimeField(db_column='Date_From', blank=True, null=True)  # Field name made lowercase.
    date_to = models.DateTimeField(db_column='Date_To', blank=True, null=True)  # Field name made lowercase.
    time_diff_miniutes = models.DecimalField(db_column='TimeDiff_Miniutes', max_digits=23, decimal_places=13, blank=True, null=True)  # Field name made lowercase.
    error_type = models.CharField(db_column='ErrorType', max_length=23, blank=True, null=True)  # Field name made lowercase.
    is_allowed_daily_duplicates = models.BooleanField(db_column='IsAllowedDailyDuplicates', blank=True, null=True)  # Field name made lowercase.
    is_excluded_absence_list = models.BooleanField(db_column='IsExcludedAbsenceList', blank=True, null=True)  # Field name made lowercase.
    is_expandable_absence_range = models.BooleanField(db_column='IsExpandableAbsenceRange', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'vewActivitiesAbsenceRecord_GSheet'
