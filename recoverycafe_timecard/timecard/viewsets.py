from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import PunchTimeSerializer
from .models import PunchTime, Volunteer


class PunchTimeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the PunchTime data.
    """
    queryset = PunchTime.objects.select_related('volunteer_id')
    serializer_class = PunchTimeSerializer

    def create(self, request, *args, **kwargs):
        # Custom error message for bad volunteer.
        volunteer_staff_id = int(request.data.get('volunteer_id'))  # This is the staff ID
        try:
            volunteer = Volunteer.objects.get(staff_id=volunteer_staff_id)
        except:
            content = {
                'status': 'NO USER',
                'msg': 'The Volunteer ID {} does not exist.'.format(
                        volunteer_staff_id)
            }
            return Response(content)
        volunteer_auto_id = volunteer.pk
        data_dict_copy = request.data.copy()
        data_dict_copy['volunteer_id'] = volunteer_auto_id  # Auto-increment ID for volunteer model
        serializer = self.get_serializer(data=data_dict_copy)
        if serializer.is_valid():
            # volunteer_staff_id = serializer.validated_data.get('volunteer_pk_id')
            branch_id = serializer.validated_data.get('branch_id')
            task_id = serializer.validated_data.get('task_id')
            punch_type = serializer.validated_data.get('punch_type')

            last_punch = PunchTime.objects.filter(volunteer_id=volunteer_auto_id
                    ).order_by('-punch_time').first()

            # Handle never ever logged in, and trying to log out
            if last_punch is None:
                if punch_type == 'OUT':
                    content = {
                        'status': 'ERROR',
                        'msg': 'You cannot logout if you\'ve never logged in...'
                    }
                    return Response(content)
            else:
                # Duplicate punch types.
                if last_punch.punch_type == punch_type:
                    if punch_type == 'IN':
                        # JSON that says you're already logged in.
                        content = {
                            'status': 'DUPLICATE',
                            'msg': 'You already logged in at {}'.format(
                                    last_punch.punch_time.strftime('%c'))
                        }
                        return Response(content)
                    else:
                        # JSON that says you already logged out.
                        content = {
                            'status': 'DUPLICATE',
                            'msg': 'You already logged out at {}'.format(
                                    last_punch.punch_time.strftime('%c'))
                        }
                        return Response(content)

        request.data._mutable = True  # See if there's a better way
        request.data['volunteer_id'] = volunteer_auto_id  # Switch volunteer_id from staff ID to foreign key value
        request.POST._mutable = True  # See if there's a better way
        request.POST['volunteer_id'] = volunteer_auto_id  # Switch volunteer_id from staff ID to foreign key value
        return super(PunchTimeViewSet, self).create(request, *args, **kwargs)
