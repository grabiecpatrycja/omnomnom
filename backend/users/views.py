from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import F, Case, When, FloatField, ExpressionWrapper, IntegerField
from django.db.models.functions import Power, Round, Now, TruncDate, Floor
from users.models import UserProfile
from users.serializers import *
from datetime import timedelta



class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if User.objects.filter(email=serializer.validated_data['email']).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        if UserProfile.objects.filter(user=self.request.user).exists():
            raise ValidationError('User profile already exists.')

        serializer.save(user=self.request.user)

class Calculate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):

        result = (UserProfile.objects.filter(user=self.request.user)
                .annotate(age=Floor(
                    ExpressionWrapper(
                    (TruncDate(Now())-F('birthdate'))/timedelta(days=1)/365.25,
                    output_field=FloatField())
                ))
                .annotate(BMI=Round(F('weight')/(Power(F('height')/100, 2)),2))
                .annotate(BMR=Case(
                    When(gender='F', then=10*F('weight')+6.25*F('height')-5*F('age')-161),
                    When(gender='M', then=(10*F('weight')+6.25*F('height')-5*F('age')+5)),
                    output_field=IntegerField()
                ))
                .annotate(TDEE=Round(F('BMR')*F('activity'),0))
                .values('age','BMI', 'BMR', 'TDEE')
            )

        return Response(result)
        