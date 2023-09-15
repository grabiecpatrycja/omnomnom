from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from app_1.models import Nutrition

class NutritionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_object(self):
        data = {'name': 'test_nutrition'}
        url = reverse('nutritions-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Nutrition.objects.count(), 1)

    def test_get_all_objects(self):
        Nutrition.objects.create(name='test_nutrition')
        Nutrition.objects.create(name='test_nutrition_2')
        url = reverse('nutritions-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Nutrition.objects.count(), 2)

    def test_get_single_object(self):
        object = Nutrition.objects.create(name='test_nutrition')
        url = reverse('nutritions-detail', args=[object.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_nutrition')

    def test_update_object(self):
        object = Nutrition.objects.create(name='test_nutrition')
        updated_data = {'name': 'new_name'}
        url = reverse('nutritions-detail', args=[object.id])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        object.refresh_from_db()
        self.assertEqual(response.data['name'], 'new_name')

    def test_delete_object(self):
        object = Nutrition.objects.create(name='test_nutrition')
        url = reverse('nutritions-detail', args=[object.id])
        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Nutrition.DoesNotExist):
            object.refresh_from_db()
   
