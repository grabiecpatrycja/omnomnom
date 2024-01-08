from rest_framework import serializers
from app_1.models import *

class NutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrition
        fields = '__all__'

class ProductNutritionSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    nutrition_name = serializers.StringRelatedField(source='nutrition.name',read_only=True)
    class Meta:
        model = ProductNutrition
        fields = ['product', 'nutrition', 'nutrition_name', 'value']

class ProductSerializer(serializers.ModelSerializer):
    nutrition_entries = ProductNutritionSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class EatenRecordSerializer(serializers.Serializer):
    mass = serializers.FloatField()
    date = serializers.DateTimeField(required=False, format="%Y-%m-%dT%H:%M:%SZ")

class ContainerProductSerialzier(serializers.ModelSerializer):
    container = serializers.PrimaryKeyRelatedField(read_only=True)
    product_name = serializers.StringRelatedField(source='product.name', read_only=True)
    class Meta:
        model = ContainerProduct
        fields = ['container', 'product', 'product_name', 'mass']

class ContainerSerializer(serializers.ModelSerializer):
    product_entries = ContainerProductSerialzier(many=True, read_only=True)
    class Meta:
        model = Container
        fields = '__all__'

class ContainerMassSerializer(serializers.ModelSerializer):
    container = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = ContainerMass
        fields = '__all__'