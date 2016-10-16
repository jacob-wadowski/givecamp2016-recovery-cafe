from datetime import datetime

from rest_framework import serializers

from .models import PunchTime

class PunchTimeSerializer(serializers.ModelSerializer):
    """
    REST API for PunchTime
    """
    class Meta:
        model = PunchTime
        fields = ('id', 'volunteer_id', 'task_id', 'branch_id',
                'punch_type', 'punch_time', 'flags', 'last_modified',)
