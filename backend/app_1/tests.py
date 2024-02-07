from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from app_1.models import *
from datetime import datetime
import pytz

class NutritionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.otheruser = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.force_authenticate(user=self.user)

    def test_no_authentication(self):
        self.client.force_authenticate(user=None)
        url = reverse('nutritions-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_object(self):
        data = {'name': 'test_nutrition'}
        url = reverse('nutritions-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Nutrition.objects.count(), 1)

    def test_get_all_objects(self):
        Nutrition.objects.create(name='test_nutrition', user=self.user)
        Nutrition.objects.create(name='test_nutrition_2', user=self.user)
        Nutrition.objects.create(name='test_nutrion_3', user=self.otheruser)
        url = reverse('nutritions-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset_list = response.json()
        self.assertEqual(len(queryset_list), 2)
        for item in queryset_list:
            nutrition = Nutrition.objects.get(name=item['name'])
            self.assertEqual(nutrition.user, self.user)

    def test_get_single_object(self):
        object = Nutrition.objects.create(name='test_nutrition', user=self.user)
        url = reverse('nutritions-detail', args=[object.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_nutrition')

    def test_update_object(self):
        object = Nutrition.objects.create(name='test_nutrition', user=self.user)
        updated_data = {'name': 'new_name'}
        url = reverse('nutritions-detail', args=[object.id])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        object.refresh_from_db()
        self.assertEqual(response.data['name'], 'new_name')

    def test_delete_object(self):
        object = Nutrition.objects.create(name='test_nutrition', user=self.user)
        Nutrition.objects.create(name='test_nutrion_2', user=self.otheruser)
        url = reverse('nutritions-detail', args=[object.id])
        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Nutrition.objects.count(), 1)
        with self.assertRaises(Nutrition.DoesNotExist):
            object.refresh_from_db()
        

class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.otheruser = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.force_authenticate(user=self.user)

    def test_no_authentication(self):
        self.client.force_authenticate(user=None)
        url = reverse('products-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_object(self):
        data = {'name': 'test_product'}
        url = reverse('products-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    def test_get_all_objects(self):
        Product.objects.create(name='test_product', user=self.user)
        Product.objects.create(name='test_product_2', user=self.user)
        Product.objects.create(name='test_product_3', user=self.otheruser)
        url = reverse('products-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset_list = response.json()
        self.assertEqual(len(queryset_list), 2)
        for item in queryset_list:
            product = Product.objects.get(name=item['name'])
            self.assertEqual(product.user, self.user)

    def test_get_single_object(self):
        object = Product.objects.create(name='test_product', user=self.user)
        url = reverse('products-detail', args=[object.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_product')

    def test_update_object(self):
        object = Product.objects.create(name='test_product', user=self.user)
        updated_data = {'name': 'new_name'}
        url = reverse('products-detail', args=[object.id])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        object.refresh_from_db()
        self.assertEqual(response.data['name'], 'new_name')

    def test_delete_object(self):
        object = Product.objects.create(name='test_product', user=self.user)
        Product.objects.create(name='test_product', user=self.otheruser)
        url = reverse('products-detail', args=[object.id])
        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)
        with self.assertRaises(Product.DoesNotExist):
            object.refresh_from_db()


class ProductNutritionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.otheruser = User.objects.create_user(username='otheruser', password='otherpassword')
        self.product = Product.objects.create(name='test_product', user=self.user)
        self.nutrition_1 = Nutrition.objects.create(name='test_nutrition_1', user=self.user)
        self.nutrition_2 = Nutrition.objects.create(name='test_nutrition_2', user=self.user)
        self.nutrition_3 = Nutrition.objects.create(name='test_nutrition_3', user=self.otheruser)

        self.client.force_authenticate(user=self.user)

    def test_create_object(self):
        data = [
                {'nutrition': self.nutrition_1.id, 'value': 120},
                {'nutrition': self.nutrition_2.id, 'value': 40}
            ]
        url = reverse('products-nutritions', args=[self.product.id])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductNutrition.objects.count(), 2)

    def test_create_object_otheruser(self):
        data = [
                {'nutrition': self.nutrition_1.id, 'value': 120},
                {'nutrition': self.nutrition_3.id, 'value': 40}
            ]
        url = reverse('products-nutritions', args=[self.product.id])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ProductNutrition.objects.count(), 0)

    def test_create_object_error(self):
        data = [
                {'nutrition': self.nutrition_1.id, 'value': 120},
                {'nutrition': self.nutrition_2.id, 'value': "króliczek"}
                ]
        url = reverse('products-nutritions', args=[self.product.id])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ProductNutrition.objects.count(), 0)

    def test_update_object(self):
        ProductNutrition.objects.create(product=self.product, nutrition=self.nutrition_1, value=120)
        updated_data = [
                {'nutrition': self.nutrition_1.id, 'value': 120}, 
                {'nutrition': self.nutrition_2.id, 'value': 40}
                ]
        url = reverse('products-nutritions', args=[self.product.id])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        object_1 = ProductNutrition.objects.get(nutrition=self.nutrition_1)
        object_2 = ProductNutrition.objects.get(nutrition=self.nutrition_2)
        self.assertEqual(object_1.value, 120)
        self.assertEqual(object_2.value, 40)
        self.assertEqual(ProductNutrition.objects.count(), 2)


class EatenRecordTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(name='test_product', user=self.user)

        self.client.force_authenticate(user=self.user)

    def test_create_object(self):
        data = {'mass': 100}
        url = reverse('products-eat', args=[self.product.id])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContainerMass.objects.count(), 2)
        eaten = ContainerMass.objects.latest('date')
        self.assertLessEqual(eaten.date - timezone.now(), timezone.timedelta(seconds=1))
    
    def test_create_object_with_date(self):
        custom_date = datetime(1989, 2, 24, 11, 30, 00, tzinfo=pytz.utc)
        data = {'mass': 100, 'date': custom_date.isoformat()}
        url = reverse('products-eat', args=[self.product.id])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContainerMass.objects.count(), 2)
        eaten= ContainerMass.objects.latest('date')
        self.assertLessEqual(eaten.date - custom_date, timezone.timedelta(seconds=1))


class ContainerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.otheruser = User.objects.create_user(username='otheruser', password='otherpassword')

        self.client.force_authenticate(user=self.user)

    def test_no_authentication(self):
        self.client.force_authenticate(user=None)
        url = reverse('containers-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_object(self):
        data = {'name': 'test_container'}
        url = reverse('containers-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Container.objects.count(), 1)

    def test_get_all_objects(self):
        Container.objects.create(name='test_container_1', user=self.user)
        Container.objects.create(name='test_container_2', user = self.user)
        Container.objects.create(name='test_container_3', user = self.otheruser)
        url = reverse('containers-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset_list = response.json()
        self.assertEqual(len(queryset_list), 2)
        for item in queryset_list:
            nutrition = Container.objects.get(name=item['name'])
            self.assertEqual(nutrition.user, self.user)

    def test_get_single_object(self):
        object = Container.objects.create(name='test_container', user=self.user)
        url = reverse('containers-detail', args=[object.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_container')

    def test_update_object(self):
        object = Container.objects.create(name='test_container', user=self.user)
        updated_data = {'name': 'new_name'}
        url = reverse('containers-detail', args=[object.id])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        object.refresh_from_db()
        self.assertEqual(response.data['name'], 'new_name')

    def test_delete_object(self):
        object = Container.objects.create(name='test_container', user=self.user)
        Container.objects.create(name='test_container', user=self.otheruser)
        url = reverse('containers-detail', args=[object.id])
        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Container.objects.count(), 1)
        with self.assertRaises(Container.DoesNotExist):
            object.refresh_from_db()


class ContainerProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.otheruser = User.objects.create_user(username='otheruser', password='otherpassword')
        self.container = Container.objects.create(name='test_container', user=self.user)
        self.product_1 = Product.objects.create(name='test_product_1', user=self.user)
        self.product_2 = Product.objects.create(name='test_product_2', user=self.user)
        self.product_3 = Product.objects.create(name='test_product_3', user=self.otheruser)

        self.client.force_authenticate(user=self.user)

    def test_create_object(self):
        data = [
                {'product': self.product_1.id, 'mass': 100},
                {'product': self.product_2.id, 'mass': 20}
            ]
        url = reverse('containers-products', args=[self.container.id])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContainerProduct.objects.count(), 2)
    
    def test_create_object_otheruser(self):
        data = [
                {'product': self.product_1.id, 'value': 120},
                {'product': self.product_3.id, 'value': 40}
            ]
        url = reverse('containers-products', args=[self.container.id])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ContainerProduct.objects.count(), 0)

    def test_create_object_error(self):
        data = [
            {'product': self.product_1.id, 'mass': 100},
            {'product': self.product_2.id, 'mass': "pingwinek"}
            ]
        url = reverse('containers-products', args=[self.container.id])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ContainerProduct.objects.count(), 0)

    def test_update_object(self):
        ContainerProduct.objects.create(container=self.container, product=self.product_1, mass=100)
        ContainerProduct.objects.create(container=self.container, product=self.product_2, mass=200)
        updated_data = [
            {'product': self.product_1.id, 'mass': 120}
            ]
        url = reverse('containers-products', args=[self.container.id])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        object = ContainerProduct.objects.get(product=self.product_1)
        self.assertEqual(object.mass, 120)
        self.assertEqual(ContainerProduct.objects.count(), 1)

class ContainerMassTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.container = Container.objects.create(name='test_container', user=self.user)

        self.client.force_authenticate(user=self.user)

    def test_get_objects(self):
        ContainerMass.objects.create(container=self.container, mass=500)
        ContainerMass.objects.create(container=self.container, mass=400)
        url = reverse('containers-mass', args=[self.container.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ContainerMass.objects.count(), 2)        

    def test_create_object(self):
        data = {'mass': 500}
        url = reverse('containers-mass', args=[self.container.id])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContainerMass.objects.count(), 1)
        container_mass = ContainerMass.objects.latest('date')
        self.assertLessEqual(container_mass.date - timezone.now(), timezone.timedelta(seconds=1))

    def test_create_object_with_date(self):
        custom_date = datetime(1989, 2, 24, 11, 30, tzinfo=pytz.utc)
        data = {'mass': 100, 'date': custom_date.isoformat()}
        url = reverse('containers-mass', args=[self.container.id])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContainerMass.objects.count(), 1)
        container_mass = ContainerMass.objects.latest('date')
        self.assertEqual(container_mass.date, custom_date)

    def test_delete_object(self):
        object_1 = ContainerMass.objects.create(container=self.container, mass=200)
        object_2 = ContainerMass.objects.create(container=self.container, mass=100)
        url = reverse('containers-mass', args=[self.container.id])
        response = self.client.delete(url, {'id': [object_2.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ContainerMass.objects.count(), 1)


class logTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.otheruser = User.objects.create(username='otheruser', password='otherpassword')
        today = timezone.now()
        yesterday = timezone.now() - timezone.timedelta(days=1)
        self.nutrition_1 = Nutrition.objects.create(name='nutrition_1', user=self.user)
        self.nutrition_2 = Nutrition.objects.create(name='nutriton_2', user=self.user)
        self.nutrition_3 = Nutrition.objects.create(name='nutrition_3', user=self.otheruser)
        self.product_1 = Product.objects.create(name='product_1', user=self.user)
        self.product_2 = Product.objects.create(name='product_2', user=self.user)
        self.product_3 = Product.objects.create(name='product_3', user=self.user)
        self.product_4 = Product.objects.create(name='product_4', user=self.otheruser)
        ProductNutrition.objects.create(product=self.product_1, nutrition=self.nutrition_1, value=100)
        ProductNutrition.objects.create(product=self.product_1, nutrition=self.nutrition_2, value=10)
        ProductNutrition.objects.create(product=self.product_2, nutrition=self.nutrition_1, value=200)
        ProductNutrition.objects.create(product=self.product_2, nutrition=self.nutrition_2, value=20)
        ProductNutrition.objects.create(product=self.product_3, nutrition=self.nutrition_1, value=50)
        ProductNutrition.objects.create(product=self.product_3, nutrition=self.nutrition_2, value=5)
        ProductNutrition.objects.create(product=self.product_4, nutrition=self.nutrition_3, value=150)
        self.container_1 = Container.objects.create(name='jar_1', user=self.user)
        self.container_2 = Container.objects.create(name='jar_2', user=self.user)
        self.container_3 = Container.objects.create(name='jar_3', user=self.otheruser)
        ContainerProduct.objects.create(container=self.container_1, product=self.product_1, mass=500)
        ContainerProduct.objects.create(container=self.container_1, product=self.product_2, mass=500)
        ContainerProduct.objects.create(container=self.container_2, product=self.product_1, mass=500)
        ContainerProduct.objects.create(container=self.container_2, product=self.product_2, mass=500)
        ContainerProduct.objects.create(container=self.container_3, product=self.product_4, mass=500)

        for container in [self.container_1, self.container_2, self.container_3]:
            ContainerMass.objects.create(container=container, mass=500, date=yesterday)
            ContainerMass.objects.create(container=container, mass=450, date=yesterday + timezone.timedelta(minutes=1))
            ContainerMass.objects.create(container=container, mass=420, date=today)
            ContainerMass.objects.create(container=container, mass=400, date=today + timezone.timedelta(minutes=1))

        self.client.force_authenticate(user=self.user)

    def test_one_container(self):
        url = reverse('log')
        response = self.client.get(url, {'containers': [self.container_1.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset_list = response.json()
        self.assertEqual(queryset_list, [{'nutrition': 1, 'total_nutrition': 75.0}, {'nutrition': 2, 'total_nutrition': 7.5}])

    def test_two_containers(self):
        url = reverse('log')
        response = self.client.get(url, {'containers': [self.container_1.id, self.container_2.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset_list = response.json()
        self.assertEqual(queryset_list, [{'nutrition': 1, 'total_nutrition': 150.0}, {'nutrition': 2, 'total_nutrition': 15.0}])
    
    def test_otheruser(self):
        url = reverse('log')
        response = self.client.get(url, {'containers': [self.container_1.id, self.container_3.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)