# TimesheetApp/api_views.py
from rest_framework import viewsets, permissions, filters
from .models import vewTaskLog
from .serializers import TaskLogWriteSerializer, TaskLogReadSerializer

class TaskLogViewSet(viewsets.ModelViewSet):
    """
    GET -> reads from vewTaskLog (denormalised view)
    POST/PUT/PATCH -> writes to tbltasklog via TaskLogWriteSerializer
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    # Order/search on the new field names
    ordering_fields = ['activity_date', 'activity_time', 'action_timestamp', 'id']
    search_fields = ['remarks', 'work_activities', 'task', 'role', 'user_key']

    def get_queryset(self):
        qs = vewTaskLog.objects.all().order_by('-activity_date', '-activity_time', '-id')

        # Optional filters: ?fk_userID=4&year=2025&from=2025-08-01&to=2025-08-31
        fk_user = self.request.query_params.get('fk_userID')
        if fk_user:
            qs = qs.filter(fk_userID=fk_user)

        year = self.request.query_params.get('year')
        if year:
            qs = qs.filter(activity_date__year=int(year))

        date_from = self.request.query_params.get('from')
        if date_from:
            qs = qs.filter(activity_date__gte=date_from)

        date_to = self.request.query_params.get('to')
        if date_to:
            qs = qs.filter(activity_date__lte=date_to)

        return qs

    def get_serializer_class(self):
        # Use write serializer on mutations, read serializer otherwise
        if self.action in ['create', 'update', 'partial_update']:
            return TaskLogWriteSerializer
        return TaskLogReadSerializer
