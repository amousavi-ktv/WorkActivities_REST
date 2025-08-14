# TimesheetApp/api_views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import (
    vewTaskLogAdmin,
    vewTaskLogSupervisor,
    vewTaskLogStaff,
    vewUserDetails,
    vewActivitiesTimesheetFullRange_GSheet,
)

from .serializers import (
    vewTaskLogAdminSerializer,
    vewTaskLogSupervisorSerializer,
    vewTaskLogStaffSerializer,
    vewUserDetailsSerializer,
    vewTimesheetSerializer,
)

class vewTaskLogAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = vewTaskLogAdmin.objects.all()
    serializer_class = vewTaskLogAdminSerializer
    permission_classes = [IsAuthenticated]


class vewTaskLogSupervisorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = vewTaskLogSupervisor.objects.all()
    serializer_class = vewTaskLogSupervisorSerializer
    permission_classes = [IsAuthenticated]


class vewTaskLogStaffViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = vewTaskLogStaff.objects.all()
    serializer_class = vewTaskLogStaffSerializer
    permission_classes = [IsAuthenticated]


class vewUserDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = vewUserDetails.objects.all()
    serializer_class = vewUserDetailsSerializer
    permission_classes = [IsAuthenticated]


class vewTimesheetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Optional filters (query params):
      - employee_id
      - activity_date__gte
      - activity_date__lte
    """
    queryset = vewActivitiesTimesheetFullRange_GSheet.objects.all()
    serializer_class = vewTimesheetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = vewActivitiesTimesheetFullRange_GSheet.objects.all()
        employee_id = self.request.query_params.get("employee_id") or None
        date_from = self.request.query_params.get("activity_date__gte") or None
        date_to = self.request.query_params.get("activity_date__lte") or None

        if employee_id:
            qs = qs.filter(employee_id=employee_id)
        if date_from:
            qs = qs.filter(activity_date__gte=date_from)
        if date_to:
            qs = qs.filter(activity_date__lte=date_to)

        return qs

    # Note: The above code assumes that the serializers for the viewsets are defined in a file named serializers.py
    # and that the models are defined in models.py as per Django conventions.

