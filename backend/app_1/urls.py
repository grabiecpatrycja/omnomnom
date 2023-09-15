from rest_framework.routers import DefaultRouter
from app_1.views import NutritionViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'nutritions', NutritionViewSet, basename="nutritions")
router.register(r'products', ProductViewSet)
urlpatterns = router.urls