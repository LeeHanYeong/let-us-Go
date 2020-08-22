from rest_framework import status
from rest_framework.test import APITestCase


class UserAPIViewTest(APITestCase):
    URL = "/v1/members/users/"

    def test_request_methods(self):
        self.assertEqual(
            self.client.patch(self.URL).status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
        )
        self.assertEqual(
            self.client.put(self.URL).status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
        )
        self.assertEqual(
            self.client.delete(self.URL).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
