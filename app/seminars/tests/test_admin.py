from django.test import TestCase
from model_bakery import baker
from rest_framework import status

from members.models import User
from seminars.models import Seminar, Track, Session, Speaker


class AdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make(User, is_staff=True, is_superuser=True)

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_seminar(self):
        seminars = baker.make(Seminar, _quantity=10)
        url_list = "/admin/seminars/seminar/"
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url_change = f"/admin/seminars/seminar/{seminars[0].id}/change/"
        response = self.client.get(url_change)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_track(self):
        tracks = baker.make(Track, _quantity=10)
        url_list = "/admin/seminars/track/"
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url_change = f"/admin/seminars/track/{tracks[0].id}/change/"
        response = self.client.get(url_change)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_session(self):
        sessions = baker.make(Session, _quantity=10)
        url_list = "/admin/seminars/session/"
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url_change = f"/admin/seminars/session/{sessions[0].id}/change/"
        response = self.client.get(url_change)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_speaker(self):
        speakers = baker.make(Speaker, _quantity=10)
        url_list = "/admin/seminars/speaker/"
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url_change = f"/admin/seminars/speaker/{speakers[0].id}/change/"
        response = self.client.get(url_change)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
