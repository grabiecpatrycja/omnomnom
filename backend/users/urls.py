from rest_framework.routers import DefaultRouter
from django.urls import path
from users.views import *
from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register(r'userprofile', UserProfileViewSet, basename="userprofile")

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('token', TokenObtainPairView.as_view(), name='token'),
    path('calculate', Calculate.as_view(), name='calculate')
]
urlpatterns += router.urls

