from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'passowrd':{'write_only': True}}

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
        user = serializers.PrimaryKeyRelatedField(read_only=True)
        
        class Meta:
            model = UserProfile
            fields = '__all__'
            