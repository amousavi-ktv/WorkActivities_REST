
from rest_framework import serializers
from .models import (
    vewTaskLogAdmin, vewTaskLogSupervisor, vewTaskLogStaff, vewUserDetails, vewActivitiesTimesheetFullRange_GSheet
)
class vewTaskLogAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = vewTaskLogAdmin
        fields = '__all__'

class vewTaskLogSupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = vewTaskLogSupervisor
        fields = '__all__'

class vewTaskLogStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = vewTaskLogStaff
        fields = '__all__'

class vewUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = vewUserDetails
        fields = '__all__'

class vewTimesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = vewActivitiesTimesheetFullRange_GSheet
        fields = '__all__'
