from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from app_1.models import *
from datetime import datetime
import pytz

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
   

class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_object(self):
        data = {'name': 'test_product'}
        url = reverse('products-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    def test_get_all_objects(self):
        Product.objects.create(name='test_product')
        Product.objects.create(name='test_product_2')
        url = reverse('products-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 2)

    def test_get_single_object(self):
        object = Product.objects.create(name='test_product')
        url = reverse('products-detail', args=[object.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_product')

    def test_update_object(self):
        object = Product.objects.create(name='test_product')
        updated_data = {'name': 'new_name'}
        url = reverse('products-detail', args=[object.id])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        object.refresh_from_db()
        self.assertEqual(response.data['name'], 'new_name')

    def test_delete_object(self):
        object = Product.objects.create(name='test_product')
        url = reverse('products-detail', args=[object.id])
        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Product.DoesNotExist):
            object.refresh_from_db()


class ProductNutritionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(name='test_product')
        self.nutrition_1 = Nutrition.objects.create(name='test_nutrition_1')
        self.nutrition_2 = Nutrition.objects.create(name='test_nutrition_2')

    def test_create_object(self):
        data = [{'product':self.product.id, 'nutrition': self.nutrition_1.id, 'value': 120},{'product':self.product.id, 'nutrition': self.nutrition_2.id, 'value': 40}]
        url = reverse('products-nutritions', args=[self.product.id])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductNutrition.objects.count(), 2)

    def test_create_object_error(self):
        data = [{'product':self.product.id, 'nutrition': self.nutrition_1.id, 'value': 120},{'product':self.product.id, 'nutrition': self.nutrition_2.id, 'value': "króliczek"}]
        url = reverse('products-nutritions', args=[self.product.id])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ProductNutrition.objects.count(), 0)

    def test_update_object(self):
        object_1 = ProductNutrition.objects.create(product=self.product, nutrition=self.nutrition_1, value=120)
        object_2 = ProductNutrition.objects.create(product=self.product, nutrition=self.nutrition_2, value=20)
        updated_data = [{'nutrition': self.nutrition_1.id, 'value': 120}, {'nutrition': self.nutrition_2.id, 'value': 40}]
        url = reverse('products-nutritions', args=[self.product.id])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        object_1.refresh_from_db()
        self.assertEqual(object_1.value, 120)
        object_2.refresh_from_db()
        self.assertEqual(object_2.value, 40)
        self.assertEqual(ProductNutrition.objects.count(), 2)


class EatenRecordTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(name='test_product')
    
    def test_create_object(self):
        data = {'product':self.product.id, 'mass': 100}
        url = reverse('products-eat', args=[self.product.id])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContainerMass.objects.count(), 2)
        eaten = ContainerMass.objects.latest('date')
        self.assertLessEqual(eaten.date - timezone.now(), timezone.timedelta(seconds=1))
    
    def test_create_object_with_date(self):
        custom_date = datetime(1989, 2, 24, 11, 30, 00, tzinfo=pytz.utc)
        data = {'product':self.product.id, 'mass': 100, 'date': custom_date.isoformat()}
        url = reverse('products-eat', args=[self.product.id])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContainerMass.objects.count(), 2)
        eaten= ContainerMass.objects.latest('date')
        self.assertLessEqual(eaten.date - custom_date, timezone.timedelta(seconds=1))


class ContainerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_object(self):
        data = {'name': 'test_container'}
        url = reverse('containers-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Container.objects.count(), 1)

    def test_get_all_objects(self):
        Container.objects.create(name='test_container_1')
        Container.objects.create(name='test_container_2')
        url = reverse('containers-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Container.objects.count(), 2)

    def test_get_single_object(self):
        object = Container.objects.create(name='test_container')
        url = reverse('containers-detail', args=[object.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_container')

    def test_update_object(self):
        object = Container.objects.create(name='test_container')
        updated_data = {'name': 'new_name'}
        url = reverse('containers-detail', args=[object.id])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        object.refresh_from_db()
        self.assertEqual(response.data['name'], 'new_name')

    def test_delete_object(self):
        object = Container.objects.create(name='test_container')
        url = reverse('containers-detail', args=[object.id])
        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Container.DoesNotExist):
            object.refresh_from_db()


class ContainerProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.container = Container.objects.create(name='test_container')
        self.product_1 = Product.objects.create(name='test_product_1')
        self.product_2 = Product.objects.create(name='test_product_2')
        self.product_3 = Product.objects.create(name='test_product_3')

    def test_create_object(self):
        data = [{'container':self.container.id, 'product': self.product_1.id, 'mass': 100},{'container':self.container.id, 'product': self.product_2.id, 'mass': 20}]
        url = reverse('containers-products', args=[self.container.id])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContainerProduct.objects.count(), 2)

    def test_create_object_error(self):
        data = [{'container':self.container.id, 'product': self.product_1.id, 'mass': 100},{'container':self.container.id, 'product': self.product_2.id, 'mass': "pingwinek"}]
        url = reverse('containers-products', args=[self.container.id])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ContainerProduct.objects.count(), 0)

    def test_update_object(self):
        object_1 = ContainerProduct.objects.create(container=self.container, product=self.product_1, mass=100)
        object_2 = ContainerProduct.objects.create(container=self.container, product=self.product_2, mass=200)
        object_3 = ContainerProduct.objects.create(container=self.container, product=self.product_3, mass=20)
        updated_data = [{'product': self.product_1.id, 'mass': 100}, {'product': self.product_2.id, 'mass': 180}]
        url = reverse('containers-products', args=[self.container.id])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        container_product = ContainerProduct.objects.get(product=self.product_2)
        self.assertEqual(container_product.mass, 180)
        self.assertEqual(ContainerProduct.objects.count(), 2)

class ContainerMassTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.container = Container.objects.create(name='test_container')

    def test_get_objects(self):
        ContainerMass.objects.create(container=self.container, mass=500)
        ContainerMass.objects.create(container=self.container, mass=400)
        url = reverse('containers-mass', args=[self.container.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ContainerMass.objects.count(), 2)        

    def test_create_object(self):
        data = {'container':self.container.id, 'mass': 500}
        url = reverse('containers-mass', args=[self.container.id])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContainerMass.objects.count(), 1)
        container_mass = ContainerMass.objects.latest('date')
        self.assertLessEqual(container_mass.date - timezone.now(), timezone.timedelta(seconds=1))

    def test_create_object_with_date(self):
        custom_date = datetime(1989, 2, 24, 11, 30, tzinfo=pytz.utc)
        data = {'container':self.container.id, 'mass': 100, 'date': custom_date.isoformat()}
        url = reverse('containers-mass', args=[self.container.id])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContainerMass.objects.count(), 1)
        container_mass = ContainerMass.objects.latest('date')
        self.assertEqual(container_mass.date, custom_date)

class logTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_1container(self):
        today = timezone.now()
        yesterday = timezone.now() - timezone.timedelta(days=1)
        nutrition_1 = Nutrition.objects.create(name='nutrition_1')
        nutrition_2 = Nutrition.objects.create(name='nutriton_2')
        product_1 = Product.objects.create(name='product_1')
        product_2 = Product.objects.create(name='product_2')
        product_3 = Product.objects.create(name='not_in_container')
        ProductNutrition.objects.create(product=product_1, nutrition=nutrition_1, value=100)
        ProductNutrition.objects.create(product=product_1, nutrition=nutrition_2, value=10)
        ProductNutrition.objects.create(product=product_2, nutrition=nutrition_1, value=200)
        ProductNutrition.objects.create(product=product_2, nutrition=nutrition_2, value=20)
        ProductNutrition.objects.create(product=product_3, nutrition=nutrition_1, value=50)
        ProductNutrition.objects.create(product=product_3, nutrition=nutrition_2, value=5)
        container = Container.objects.create(name='jar')
        ContainerProduct.objects.create(container=container, product=product_1, mass=500)
        ContainerProduct.objects.create(container=container, product=product_2, mass=500)
        ContainerMass.objects.create(container=container, mass=500, date=yesterday)
        ContainerMass.objects.create(container=container, mass=450, date=yesterday + timezone.timedelta(minutes=1))
        ContainerMass.objects.create(container=container, mass=420, date=today)
        ContainerMass.objects.create(container=container, mass=400, date=today + timezone.timedelta(minutes=1))

        url = reverse('log')
        response = self.client.get(url, {'containers': [container.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset_list = response.json()
        self.assertEqual(queryset_list, [{'nutrition': 1, 'total_nutrition': 75.0}, {'nutrition': 2, 'total_nutrition': 7.5}])

    def test_2containers(self):
        today = timezone.now()
        yesterday = timezone.now() - timezone.timedelta(days=1)
        nutrition_1 = Nutrition.objects.create(name='nutrition_1')
        nutrition_2 = Nutrition.objects.create(name='nutriton_2')
        product_1 = Product.objects.create(name='product_1')
        product_2 = Product.objects.create(name='product_2')
        product_3 = Product.objects.create(name='not_in_container')
        ProductNutrition.objects.create(product=product_1, nutrition=nutrition_1, value=100)
        ProductNutrition.objects.create(product=product_1, nutrition=nutrition_2, value=10)
        ProductNutrition.objects.create(product=product_2, nutrition=nutrition_1, value=200)
        ProductNutrition.objects.create(product=product_2, nutrition=nutrition_2, value=20)
        ProductNutrition.objects.create(product=product_3, nutrition=nutrition_1, value=50)
        ProductNutrition.objects.create(product=product_3, nutrition=nutrition_2, value=5)
        container_1 = Container.objects.create(name='jar1')
        container_2 = Container.objects.create(name='jar2')
        ContainerProduct.objects.create(container=container_1, product=product_1, mass=500)
        ContainerProduct.objects.create(container=container_2, product=product_2, mass=500)

        for container in [container_1, container_2]:
            ContainerMass.objects.create(container=container, mass=500, date=yesterday)
            ContainerMass.objects.create(container=container, mass=450, date=yesterday + timezone.timedelta(minutes=1))
            ContainerMass.objects.create(container=container, mass=420, date=today)
            ContainerMass.objects.create(container=container, mass=400, date=today + timezone.timedelta(minutes=1))

        url = reverse('log')
        response = self.client.get(url, {'containers': [container_1.id, container_2.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset_list = response.json()
        self.assertEqual(queryset_list, [{'nutrition': 1, 'total_nutrition': 150.0}, {'nutrition': 2, 'total_nutrition': 15.0}])
