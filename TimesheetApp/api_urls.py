# TimesheetApp/api_urls.py
from rest_framework.routers import DefaultRouter
from .api_views import TaskLogViewSet

router = DefaultRouter()
router.register(r'tasklog', TaskLogViewSet, basename='tasklog')
urlpatterns = router.urls
