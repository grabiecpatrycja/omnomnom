from rest_framework import serializers
from app_1.models import *

class NutritionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Nutrition
        fields = '__all__'

class ProductNutritionSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    nutrition_name = serializers.StringRelatedField(source='nutrition.name',read_only=True)

    class Meta:
        model = ProductNutrition
        fields = ['product', 'nutrition', 'nutrition_name', 'value']

    def validate(self, data):
        if self.context['request'].user != data['nutrition'].user:
            raise serializers.ValidationError()
        return data
    
class ProductSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    nutrition_entries = ProductNutritionSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class EatenRecordSerializer(serializers.Serializer):
    meals = [
        ('B', 'breakfast'),
        ('L', 'lunch'),
        ('D', 'dinner'),
        ('Sn', 'snack'),
        ('Su', 'supper')
    ]

    mass = serializers.FloatField()
    date = serializers.DateTimeField(required=False, format="%Y-%m-%dT%H:%M:%SZ")
    meal = serializers.ChoiceField(choices=meals)

class ContainerProductSerialzier(serializers.ModelSerializer):
    container = serializers.PrimaryKeyRelatedField(read_only=True)
    product_name = serializers.StringRelatedField(source='product.name', read_only=True)
    class Meta:
        model = ContainerProduct
        fields = ['container', 'product', 'product_name', 'mass']

    def validate(self, data):
        if self.context['request'].user != data['product'].user:
            raise serializers.ValidationError()
        return data

class ContainerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    product_entries = ContainerProductSerialzier(many=True, read_only=True)
    class Meta:
        model = Container
        fields = '__all__'

class ContainerMassSerializer(serializers.ModelSerializer):
    container = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = ContainerMass
        fields = '__all__'