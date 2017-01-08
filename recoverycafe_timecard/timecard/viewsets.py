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

        # Volunteer.pk is the foreign key used by PunchTime model (it's the auto-generated ID in the volunteer table, not the staff ID)
        volunteer_auto_id = volunteer.pk

        # Creating copy of request data dict in order to modify it before serializing it/validating
        # (as the staff ID needs to be switched out for the auto-generated volunteer ID)
        data_dict_copy = request.data.copy()
        data_dict_copy['volunteer_id'] = volunteer_auto_id

        serializer = self.get_serializer(data=data_dict_copy)  # Updated this code to use the modified request.data dict
        if serializer.is_valid():
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

        # Making the request object mutable, in order to update the value for 'volunteer_id' before using the request
        request.data._mutable = True
        request.POST._mutable = True

        # Modifying the request object to send the auto-generated volunteer ID in the 'volunteer_id' field
        # (it will fail otherwise, as it will try to send the staff ID for 'volunteer_id' in the PunchTime model)
        request.data['volunteer_id'] = volunteer_auto_id
        request.POST['volunteer_id'] = volunteer_auto_id

        # Setting request back to being immutable
        request.data._mutable = False
        request.POST._mutable = False

        return super(PunchTimeViewSet, self).create(request, *args, **kwargs)
