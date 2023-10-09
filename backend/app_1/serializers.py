from rest_framework import serializers
from app_1.models import Nutrition, Product, ProductNutrition, EatenRecord, Container, ContainerProduct

class NutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrition
        fields = '__all__'

class ProductNutritionSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = ProductNutrition
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    nutrition_entries = ProductNutritionSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class EatenRecordSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = EatenRecord
        fields = '__all__'

class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = '__all__'

class ContainerProductSerialzier(serializers.ModelSerializer):
    container = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = ContainerProduct
        fields = '__all__'