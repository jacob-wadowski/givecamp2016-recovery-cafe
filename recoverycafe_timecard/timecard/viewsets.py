from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import PunchTimeSerializer
from .models import PunchTime


class PunchTimeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the PunchTime data.
    """
    queryset = PunchTime.objects.all()
    serializer_class = PunchTimeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            volunteer_id = serializer.validated_data.get('volunteer_id')
            branch_id = serializer.validated_data.get('branch_id')
            task_id = serializer.validated_data.get('task_id')
            punch_type = serializer.validated_data.get('punch_type')

            last_punch = PunchTime.objects.filter(volunteer_id=volunteer_id
                    ).order_by('-punch_time').first()

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

        return super(PunchTimeViewSet, self).create(request, *args, **kwargs)
