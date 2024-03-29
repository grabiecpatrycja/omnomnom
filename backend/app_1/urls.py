from rest_framework.routers import DefaultRouter
from app_1.views import *
from django.urls import path

router = DefaultRouter()
router.register(r'nutritions', NutritionViewSet, basename="nutritions")
router.register(r'products', ProductViewSet, basename="products")
router.register(r'containers', ContainerViewSet, basename="containers")

urlpatterns = [
    path('log', log.as_view(), name='log')
]

urlpatterns += router.urls