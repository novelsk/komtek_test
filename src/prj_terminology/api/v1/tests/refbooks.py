import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from prj_terminology.models import (
    Reference,
    ReferenceVersion,
    ReferenceElement,
)


class RefBookTestCase(APITestCase):
    def setUp(self):
        today = timezone.now().date()

        self.url = '/terminology/api/v1/refbooks'
        self.user = User.objects.create_superuser('root')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.ref_book1 = Reference.objects.create(
            id=1,
            code='ref_code1',
            name='ref_book1',
            description='description1',
        )
        self.ref_book2 = Reference.objects.create(
            id=2,
            code='ref_code2',
            name='ref_book2',
            description='description2',
        )
        self.version1 = ReferenceVersion.objects.create(
            reference=self.ref_book1,
            code='ver_code1',
            start_date=(today - datetime.timedelta(days=1)),
        )
        self.version2 = ReferenceVersion.objects.create(
            reference=self.ref_book1,
            code='ver_code2',
            start_date=(today + datetime.timedelta(days=1)),
        )
        self.element1 = ReferenceElement.objects.create(
            version=self.version1,
            code='ver_el1',
            value='value1',
        )
        self.element2 = ReferenceElement.objects.create(
            version=self.version1,
            code='ver_el2',
            value='value2',
        )
        self.element3 = ReferenceElement.objects.create(
            version=self.version2,
            code='ver_el3',
            value='value3',
        )
        self.element4 = ReferenceElement.objects.create(
            version=self.version2,
            code='ver_el4',
            value='value4',
        )

    def test_ref_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'refbooks': [
                {
                    'id': 1,
                    'code': 'ref_code1',
                    'name': 'ref_book1',
                },
                {
                    'id': 2,
                    'code': 'ref_code2',
                    'name': 'ref_book2',
                }
            ]
        })

    def test_elements(self):
        response = self.client.get(
            f'{self.url}/{self.version1.id}/elements'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'elements': [
                {
                    'code': 'ver_el1',
                    'value': 'value1',
                },
                {
                    'code': 'ver_el2',
                    'value': 'value2',
                }
            ]
        })

    def test_elements_with_version(self):
        response = self.client.get(
            f'{self.url}/{self.version1.id}/elements',
            query_params={'version': self.version2.code},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'elements': [
                {
                    'code': 'ver_el3',
                    'value': 'value3',
                },
                {
                    'code': 'ver_el4',
                    'value': 'value4',
                }
            ]
        })

    def test_elements_not_eq(self):
        response = self.client.get(
            f'{self.url}/{self.version1.id}/elements'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {
            'elements': [
                {
                    'code': 'ver_el3',
                    'value': 'value3',
                },
                {
                    'code': 'ver_el2',
                    'value': 'value2',
                }
            ]
        })

    def test_check_element(self):
        response = self.client.get(
            f'{self.url}/{self.version1.id}/check_element',
            query_params={
                'code': self.element1.code,
                'value': self.element1.value,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, True)

    def test_check_element_with_version(self):
        response = self.client.get(
            f'{self.url}/{self.version1.id}/check_element',
            query_params={
                'version': self.version2.code,
                'code': self.element3.code,
                'value': self.element3.value,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, True)

    def test_check_element_not_in_version(self):
        response = self.client.get(
            f'{self.url}/{self.version1.id}/check_element',
            query_params={
                'version': self.version2.code,
                'code': self.element1.code,
                'value': self.element1.value,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, False)
