from rest_framework.routers import DefaultRouter
from .views import DistrictViewSet

router = DefaultRouter()
router.register(r'', DistrictViewSet, basename='district')

urlpatterns = router.urls
