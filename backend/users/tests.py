from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from users.models import UserProfile
from datetime import date

class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        data = {'username': 'name', 'email': 'name@email.com', 'password': 'password'}
        url = reverse('register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_wrong_email(self):
        User.objects.create(first_name='name_1', email='name@email.com', password='password1')
        data = {'first_name': 'name_2', 'email': 'name@email.com', 'password': 'password2'}
        url = reverse('register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.otheruser = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.force_authenticate(user=self.user)

    def test_no_authentication(self):
        self.client.force_authenticate(user=None)
        url = reverse('userprofile-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_profile(self):
        birth_date = date(1989, 2, 24)
        data = {'gender': 'F', 'weight': 60, 'height': 160, 'birthdate': birth_date}
        url = reverse('userprofile-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_get_profile(self):
        UserProfile.objects.create(gender='F', weight=60, height=160, birthdate='1989-02-24', user=self.user)
        UserProfile.objects.create(gender='M', weight=80, height=180, birthdate='1990-10-13', user=self.otheruser)
        url = reverse('userprofile-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset_list = response.json()
        self.assertEqual(len(queryset_list), 1)

    def test_update_profile(self):
        object = UserProfile.objects.create(gender='F', weight=60, height=160, birthdate='1989-02-24', user=self.user)
        updated_data = {'weight': 55}
        url = reverse('userprofile-detail', args=[object.id])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        object.refresh_from_db()
        self.assertEqual(response.data['weight'], 55)

    def test_delete_profile(self):
        object = UserProfile.objects.create(gender='F', weight=60, height=160, birthdate='1989-02-24', user=self.user)
        UserProfile.objects.create(gender='M', weight=80, height=180, birthdate='1990-10-13', user=self.otheruser)
        url = reverse('userprofile-detail', args=[object.id])
        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserProfile.objects.count(), 1)
        with self.assertRaises(UserProfile.DoesNotExist):
            object.refresh_from_db()
    
    def test_create_duplicate_profile(self):
        UserProfile.objects.create(gender='F', weight=80, height=170, birthdate='1990-10-13', user=self.user)
        birth_date = date(1989, 2, 24)
        data = {'gender': 'F', 'weight': 60, 'height': 160, 'birthdate': birth_date}
        url = reverse('userprofile-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserProfile.objects.count(), 1)

class CalculateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        UserProfile.objects.create(gender='F', weight=60, height=160, birthdate='1989-02-24', activity=1.6, user=self.user)

    def test_calculation(self):
        url = reverse('calculate')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset_list = response.json()
        self.assertEqual(queryset_list, [{'BMI': 23.44, 'BMR': 1264.0, 'TMR': 2022.4}])

