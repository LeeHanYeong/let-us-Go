from django.test import TestCase
from rest_framework.test import APITestCase


class APITest(APITestCase):
    def test_health(self):
        url = "/v1/utils/health/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class DocTest(TestCase):
    def test_200(self):
        url = "/doc/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_openapi(self):
        url = "/doc/?format=openapi"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ViewTest(TestCase):
    def test_index(self):
        url = "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_health_check(self):
        url = "/health/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
