from rest_framework import serializers
from app_1.models import Nutrition, Product, ProductNutrition, EatenRecord

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
    nutrition_entries = ProductNutritionSerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'

class EatenRecordSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = EatenRecord
        fields = '__all__'