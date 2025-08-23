# TimesheetApp/models.py
from django.db import models

class tblTask(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    task_key = models.CharField(db_column='TaskKey', unique=True, max_length=40, db_collation='Latin1_General_CI_AS')
    task = models.CharField(db_column='Task', unique=True, max_length=40, db_collation='Latin1_General_CI_AS')
    remarks = models.CharField(db_column='Remarks', max_length=250, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    def __str__(self):
        return self.task
    class Meta:
        managed = False
        db_table = 'tblTask'

class tblRole(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    role_key = models.CharField(db_column='RoleKey', max_length=20, db_collation='Latin1_General_CI_AS')
    role = models.CharField(db_column='Role', max_length=40, db_collation='Latin1_General_CI_AS')
    remarks = models.CharField(db_column='Remarks', max_length=250, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    def __str__(self):
        return self.role
    class Meta:
        managed = False
        db_table = 'tblRole'

class tblAppUser(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    pid = models.CharField(db_column='PID', unique=True, max_length=4, db_collation='Latin1_General_CI_AS')
    user_key = models.CharField(db_column='UserKey', unique=True, max_length=12, db_collation='Latin1_General_CI_AS')
    firstame = models.CharField(db_column='Firstame', max_length=50, db_collation='Latin1_General_CI_AS')
    surname = models.CharField(db_column='Surname', max_length=50, db_collation='Latin1_General_CI_AS')
    midname = models.CharField(db_column='MidName', max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fk_roleID = models.ForeignKey('tblRole', models.DO_NOTHING, db_column='fk_RoleID', blank=True, null=True)
    is_active = models.BooleanField(db_column='IsActive')
    email_address = models.CharField(db_column='EmailAddress', max_length=50, db_collation='Latin1_General_CI_AS')
    remarks = models.CharField(db_column='Remarks', max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    def __str__(self):
        return f"{self.pid} - {self.user_key}"
    class Meta:
        managed = False
        db_table = 'tblUser'

class tblAuthUser(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    fk_userID = models.ForeignKey('tblAppUser', db_column='fk_UserID', on_delete=models.DO_NOTHING)
    auth_provider = models.CharField(db_column='AuthProvider', max_length=20, db_collation='Latin1_General_CI_AS')
    email_address = models.CharField(db_column='ProviderUserID', max_length=255, db_collation='Latin1_General_CI_AS')
    password = models.CharField(db_column='Password', max_length=128, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    created_at = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)
    last_login_at = models.DateTimeField(db_column='LastLoginAt', blank=True, null=True)
    remarks = models.CharField(db_column='Remarks', max_length=10, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tblAuthUser'

class tblTaskLog(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    fk_userID = models.ForeignKey('tblAppUser', models.DO_NOTHING, db_column='fk_UserID')
    fk_taskID = models.ForeignKey('tblTask', models.DO_NOTHING, db_column='fk_TaskID')
    action_timestamp = models.DateTimeField(db_column='ActionTimestamp')
    activity_timestamp = models.DateTimeField(db_column='ActivityTimestamp')
    work_activities = models.CharField(db_column='WorkActivities', max_length=250, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    remarks = models.CharField(db_column='Remarks', max_length=250, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    adminID = models.CharField(db_column='AdminID', max_length=5, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'tblTaskLog'
        unique_together = (
            ('action_timestamp', 'fk_userID'),
            ('activity_timestamp', 'fk_taskID', 'fk_userID'),
        )

class vewTaskLog(models.Model):
    activity_id = models.IntegerField(db_column='ActivityID', primary_key=True)  # Field name made lowercase.
    user_key = models.CharField(db_column='UserKey', max_length=10, blank=True, null=True)  # Field name made lowercase.
    personal_id = models.CharField(db_column='Personal_ID', max_length=5, blank=True, null=True)  # Field name made lowercase.
    activity = models.CharField(db_column='Activity', max_length=80, blank=True, null=True)  # Field name made lowercase.
    task_key = models.CharField(db_column='TaskKey', max_length=80, blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=40, blank=True, null=True)  # Field name made lowercase.
    action_timestamp = models.DateTimeField(db_column='ActionTimestamp')  # Field name made lowercase.
    activity_timestamp = models.DateTimeField(db_column='ActivityTimestamp')  # Field name made lowercase.
    work_activities = models.CharField(db_column='WorkActivities', max_length=250, blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=250, blank=True, null=True)  # Field name made lowercase.
    admin_id = models.CharField(db_column='AdminID', max_length=5)  # Field name made lowercase.
    task_id = models.IntegerField(db_column='TaskID')  # Field name made lowercase.
    user_id = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    activity_date = models.DateField(db_column='ActivityDate', blank=True, null=True)  # Field name made lowercase.
    activity_time = models.TimeField(db_column='ActivityTime', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'vewTaskLog'

class tblSettings(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    parameterkey = models.CharField(db_column='ParameterKey', max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    parameter = models.CharField(db_column='Parameter', max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    value = models.TimeField(db_column='Value', blank=True, null=True)
    remarks = models.CharField(db_column='Remarks', max_length=150, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tblSetting'  # matches your DB

class vewUserDetails(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)
    pid = models.CharField(db_column='PID', max_length=4)
    user_key = models.CharField(db_column='UserKey', max_length=12)
    firstame = models.CharField(db_column='Firstame', max_length=50)
    surname = models.CharField(db_column='Surname', max_length=50)
    remarks = models.CharField(db_column='Remarks', max_length=50, blank=True, null=True)
    fk_roleID = models.IntegerField(db_column='fk_RoleID', blank=True, null=True)
    is_active = models.BooleanField(db_column='IsActive', blank=True, null=True)
    role_key = models.CharField(db_column='RoleKey', max_length=20, blank=True, null=True)
    role = models.CharField(db_column='Role', max_length=40, blank=True, null=True)
    role_remarks = models.CharField(db_column='RoleRemarks', max_length=250, blank=True, null=True)
    email_address = models.CharField(db_column='EmailAddress', max_length=50, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'vewUserDetails'

class vewActivitiesTimesheetFullRange_GSheet(models.Model):
    view_index = models.BigIntegerField(db_column='ViewIndex', primary_key=True)
    error_message = models.CharField(db_column='ErrorMessage', max_length=250, blank=True, null=True)
    employee_id = models.CharField(db_column='Employee_ID', max_length=10, blank=True, null=True)
    lunch_break_hours_field = models.DecimalField(db_column='Lunch Break (Hours)', max_digits=7, decimal_places=2, blank=True, null=True)
    break_outside_lunchtime_hours_field = models.DecimalField(db_column='Break Outside Lunchtime (Hours)', max_digits=7, decimal_places=2, blank=True, null=True)
    worked_hours_field = models.DecimalField(db_column='Worked (Hours)', max_digits=7, decimal_places=2, blank=True, null=True)
    work_target_hours_field = models.DecimalField(db_column='Work Target (Hours)', max_digits=13, decimal_places=4, blank=True, null=True)
    net_balance = models.DecimalField(db_column='NetBalance', max_digits=21, decimal_places=13, blank=True, null=True)
    activity_date = models.DateField(db_column='ActivityDate', blank=True, null=True)
    daily_target_duration = models.CharField(db_column='DailyTargetDuration', max_length=513, blank=True, null=True)
    daily_target_duration_brief_field = models.CharField(db_column='Daily Target Duration (Brief)', max_length=513, blank=True, null=True)
    daily_status = models.CharField(db_column='DailyStatus', max_length=4000, blank=True, null=True)
    absence_code = models.CharField(db_column='AbsenceCode', max_length=4000)
    work_start_time = models.DateTimeField(db_column='WorkStartTime', blank=True, null=True)
    work_end_time = models.DateTimeField(db_column='WorkEndTime', blank=True, null=True)
    lunchbreak_start_time = models.DateTimeField(db_column='LunchBreakStartTime', blank=True, null=True)
    lunchbreak_end_time = models.DateTimeField(db_column='LunchBreakEndTime', blank=True, null=True)
    late_attendance = models.DecimalField(db_column='LateAttendance', max_digits=12, decimal_places=8, blank=True, null=True)
    early_leave = models.DecimalField(db_column='EarlyLeave', max_digits=12, decimal_places=8, blank=True, null=True)
    employee_index = models.BigIntegerField(db_column='EmployeeIndex', blank=True, null=True)
    adjusted_hijri_month = models.IntegerField(db_column='AdjustedHijriMonth', blank=True, null=True)
    adjusted_hijri_day = models.IntegerField(db_column='AdjustedHijriDay', blank=True, null=True)
    adjusted_daily_target = models.DecimalField(db_column='Adjusted Daily Target', max_digits=15, decimal_places=4, blank=True, null=True)
    adjusted_net_balance_hours_field = models.DecimalField(db_column='Adjusted Net Balance (Hours)', max_digits=25, decimal_places=13, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'vewActivitiesTimesheetFullRange_GSheet'

class vewActivitiesAbsenceRecord_GSheet(models.Model):
    view_index = models.BigIntegerField(db_column='ViewIndex', primary_key=True)
    employee_id = models.CharField(db_column='Employee_ID', max_length=5, blank=True, null=True)
    activity_date = models.DateField(db_column='ActivityDate', blank=True, null=True)
    timestamp = models.DateTimeField(db_column='Timestamp', blank=True, null=True)
    absence_code = models.CharField(db_column='AbsenceCode', max_length=4000, blank=True, null=True)
    request_optioncode = models.CharField(db_column='RequestOptionCode', max_length=2, blank=True, null=True)
    approval_status = models.CharField(db_column='ApprovalStatus', max_length=50, blank=True, null=True)
    requestor_id = models.CharField(db_column='Requestor_ID', max_length=5, blank=True, null=True)
    date_from = models.DateTimeField(db_column='Date_From', blank=True, null=True)
    date_to = models.DateTimeField(db_column='Date_To', blank=True, null=True)
    time_diff_miniutes = models.DecimalField(db_column='TimeDiff_Miniutes', max_digits=23, decimal_places=13, blank=True, null=True)
    error_type = models.CharField(db_column='ErrorType', max_length=23, blank=True, null=True)
    is_allowed_daily_duplicates = models.BooleanField(db_column='IsAllowedDailyDuplicates', blank=True, null=True)
    is_excluded_absence_list = models.BooleanField(db_column='IsExcludedAbsenceList', blank=True, null=True)
    is_expandable_absence_range = models.BooleanField(db_column='IsExpandableAbsenceRange', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'vewActivitiesAbsenceRecord_GSheet'

class vewTransferViewToGoogleSheet(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    view_name = models.TextField(db_column='ViewName')
    google_sheets_id = models.TextField(db_column='GoogleSheets_ID')
    description = models.TextField(db_column='Description', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'vewTransferViewToGoogleSheet'

class vewUserKey(models.Model):
    user_key = models.CharField(db_column='UserKey', max_length=12, primary_key=True)
    def __str__(self):
        return self.user_key
    class Meta:
        managed = False
        db_table = 'vewUserKey'
