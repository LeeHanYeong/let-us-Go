from copy import deepcopy

from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from attends.models import Attend
from members.models import User
from seminars.models import Track


class AttendAPITest(APITestCase):
    URL_LIST = "/v1/attends/"
    URL_DETAIL = "/v1/attends/{id}/"

    def test_authenticated(self):
        response = self.client.get(self.URL_LIST)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_responses(self):
        user = baker.make(User)
        self.client.force_authenticate(user)

        response_list = self.client.get(self.URL_LIST)
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)

        track = baker.make(Track)
        response_create = self.client.post(
            self.URL_LIST,
            data={
                "track": track.id,
                "name": "TestName",
                "is_attend_after_party": False,
            },
            format="json",
        )
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

        attend = baker.make(Attend, user=user)
        url_detail = self.URL_DETAIL.format(id=attend.id)
        response_retrieve = self.client.get(url_detail)
        self.assertEqual(response_retrieve.status_code, status.HTTP_200_OK)

        data_attend = deepcopy(response_retrieve.data)
        data_attend["name"] = "TestName"
        response_update = self.client.patch(
            url_detail,
            data_attend,
            format="json",
        )
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_update.data["name"], "TestName")

        response_destroy = self.client.delete(url_detail)
        self.assertEqual(response_destroy.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Attend.objects.filter(id=attend.id).exists())

    def test_지원서가_이미_존재할시_error(self):
        track = baker.make(Track)
        user = baker.make(User)
        baker.make(Attend, track=track, user=user)

        self.client.force_authenticate(user)
        response = self.client.post(
            self.URL_LIST,
            data={
                "track": track.id,
                "name": "TestName",
                "is_attend_after_party": False,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
