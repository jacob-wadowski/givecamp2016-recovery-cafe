from rest_framework import viewsets, status

from .serializers import PunchTimeSerializer
from .models import PunchTime


class PunchTimeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the PunchTime data.
    """
    queryset = PunchTime.objects.all()
    serializer_class = PunchTimeSerializer