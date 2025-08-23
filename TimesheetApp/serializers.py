
# TimesheetApp/serializers.py
from rest_framework import serializers
from datetime import datetime
from .models import tblTaskLog, vewTaskLog

class TaskLogWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = tblTaskLog
        fields = [
            'id', 'fk_userID', 'fk_taskID',
            'activity_date', 'activity_time',
            'action_timestamp',
            'work_activities', 'remarks',
            'fk_operatorID',
        ]

    def validate(self, attrs):
        """
        Rules:
        - If action_timestamp is missing (STAFF path), set to now and derive activity_date/time if missing.
        - If action_timestamp is provided but activity_date/time missing, derive from action_timestamp.
        - If fk_operatorID missing, default to fk_userID (actor == subject).
        """
        at = attrs.get('action_timestamp')
        if not at:
            now = datetime.now()
            attrs['action_timestamp'] = now
            attrs.setdefault('activity_date', now.date())
            attrs.setdefault('activity_time', now.time().replace(microsecond=0))
        else:
            # normalise and derive date/time if not given
            attrs.setdefault('activity_date', at.date())
            attrs.setdefault('activity_time', at.time().replace(microsecond=0))

        if not attrs.get('fk_operatorID'):
            attrs['fk_operatorID'] = attrs['fk_userID']

        return attrs


class TaskLogReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = vewTaskLog
        fields = '__all__'
