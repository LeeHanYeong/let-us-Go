from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from seminars.models import Seminar, Track, Session, Speaker


class SeminarAPITest(APITestCase):
    URL_LIST = "/v1/seminars/"
    URL_DETAIL = "/v1/seminars/{id}/"

    def test_list(self):
        baker.make(Seminar, _quantity=10)
        response = self.client.get(self.URL_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)

    def test_retrieve(self):
        seminar = baker.make(Seminar)
        response = self.client.get(self.URL_DETAIL.format(id=seminar.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TrackAPITest(APITestCase):
    URL_LIST = "/v1/seminars/tracks/"
    URL_DETAIL = "/v1/seminars/tracks/{id}/"

    def test_list(self):
        baker.make(Track, _quantity=10)
        response = self.client.get(self.URL_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)

    def test_retrieve(self):
        track = baker.make(Track)
        response = self.client.get(self.URL_DETAIL.format(id=track.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SessionAPITest(APITestCase):
    URL_LIST = "/v1/seminars/sessions/"
    URL_DETAIL = "/v1/seminars/sessions/{id}/"

    def test_list(self):
        baker.make(Session, _quantity=10)
        response = self.client.get(self.URL_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)

    def test_retrieve(self):
        session = baker.make(Session)
        response = self.client.get(self.URL_DETAIL.format(id=session.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SpeakerAPITest(APITestCase):
    URL_LIST = "/v1/seminars/speakers/"

    def test_list(self):
        baker.make(Speaker, _quantity=10)
        response = self.client.get(self.URL_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)
