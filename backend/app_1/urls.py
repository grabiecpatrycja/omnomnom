from rest_framework.routers import DefaultRouter
from app_1.views import NutritionViewSet

router = DefaultRouter()
router.register(r'nutritions', NutritionViewSet)
urlpatterns = router.urls