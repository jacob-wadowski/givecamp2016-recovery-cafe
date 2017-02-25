from datetime import datetime

from rest_framework import serializers

from .models import PunchTime, Volunteer

class VolunteerSerializer(serializers.ModelSerializer):
    """
    REST API for Volunteer
    """
    class Meta:
        model = Volunteer
        fields = ('id', 'first_name', 'last_name', 'staff_id')


class PunchTimeSerializer(serializers.ModelSerializer):
    """
    REST API for PunchTime
    """
    volunteer = VolunteerSerializer(source="volunteer_id",
            read_only=True)

    class Meta:
        model = PunchTime
        fields = ('id', 'volunteer_id', 'volunteer', 'task_id', 'branch_id',
                'punch_type', 'punch_time', 'flags', 'last_modified', 'isAdminCheckout', 'adminCheckoutTime')

