
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    vewTaskLogAdminViewSet,
    vewTaskLogSupervisorViewSet, 
    vewTaskLogStaffViewSet,
    vewUserDetailsViewSet,
    vewTimesheetViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'tasklog-admin', vewTaskLogAdminViewSet)
router.register(r'tasklog-supervisor', vewTaskLogSupervisorViewSet)
router.register(r'tasklog-staff', vewTaskLogStaffViewSet)
router.register(r'user-details', vewUserDetailsViewSet)
router.register(r'timesheet', vewTimesheetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
