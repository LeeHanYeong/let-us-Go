from copy import deepcopy

from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from members.models import User, EmailVerification
from members.serializers import UserSerializer


class UserAPIViewTest(APITestCase):
    URL_LIST = "/v1/members/users/"
    URL_DETAIL = "/v1/members/users/{id}/"

    def test_request_methods(self):
        self.assertEqual(
            self.client.patch(self.URL_LIST).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
        self.assertEqual(
            self.client.put(self.URL_LIST).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
        self.assertEqual(
            self.client.delete(self.URL_LIST).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_response_success(self):
        user = baker.make(User)
        self.client.force_authenticate(user)

        response_list = self.client.get(self.URL_LIST)
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)

        email = "sample@sample.com"
        e = baker.make(
            EmailVerification,
            email=email,
        )
        response_create = self.client.post(
            self.URL_LIST,
            data={
                "email_verification_code": e.code,
                "password1": "SamplePassword",
                "password2": "SamplePassword",
                "type": User.TYPE_EMAIL,
                "email": email,
                "nickname": "Sample Nickname",
            },
            format="json",
        )
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

        url_detail = self.URL_DETAIL.format(id=user.id)
        response_retrieve = self.client.get(url_detail)
        self.assertEqual(response_retrieve.status_code, status.HTTP_200_OK)

        data = deepcopy(response_retrieve.data)
        data["name"] = "TestName"
        response_update = self.client.patch(url_detail, data=data, format="json")
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_update.data["name"], "TestName")

        response_profile = self.client.get(f"{self.URL_LIST}profile")
        self.assertEqual(response_profile.status_code, status.HTTP_200_OK)

        response_available_true = self.client.post(
            f"{self.URL_LIST}available/",
            data={
                "attribute_name": "email",
                "value": email,
            },
            format="json",
        )
        self.assertEqual(response_available_true.status_code, status.HTTP_200_OK)
        self.assertEqual(response_available_true.data["exists"], True)

        response_available_false = self.client.post(
            f"{self.URL_LIST}available/",
            data={
                "attribute_name": "name",
                "value": "a" + email,
            },
            format="json",
        )
        self.assertEqual(response_available_false.status_code, status.HTTP_200_OK)
        self.assertEqual(response_available_false.data["exists"], False)

    def test_permissions(self):
        # List요청, 인증필요
        response = self.client.get(self.URL_LIST)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Retrieve요청, 인증필요
        user = baker.make(User)
        response = self.client.get(self.URL_DETAIL.format(id=user.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Profile요청, 인증 필요
        response = self.client.get(self.URL_LIST + "profile/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Retrieve요청, 다른사용자일 경우 거부
        user2 = baker.make(User)
        self.client.force_authenticate(user2)
        response = self.client.get(self.URL_DETAIL.format(id=user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Update요청, 다른사용자일 경우 거부
        data = UserSerializer(user).data
        data["name"] = "AnotherName"
        response = self.client.patch(
            self.URL_DETAIL.format(id=user.id), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Destroy요청, 허용되지 않는 요청
        response = self.client.delete(self.URL_DETAIL.format(id=user.id))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class UserProfileAPITest(APITestCase):
    URL = "/v1/members/users/profile/"

    def test_response_data_fields(self):
        user = baker.make(User)
        self.client.force_authenticate(user)

        response = self.client.get(self.URL)
        for field in ["username", "type", "name", "nickname", "email", "phone_number"]:
            self.assertIn(field, response.data)
