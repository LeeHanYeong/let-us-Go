from itertools import cycle

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

    def test_retrieve_recent_when_id_0(self):
        baker.make(Seminar, _quantity=10)
        first_seminar = Seminar.objects.first()
        response = self.client.get(self.URL_DETAIL.format(id=0))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], first_seminar.id)


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

    def test_search(self):
        baker.make(Session, name="letusgo")
        response = self.client.get(
            self.URL_LIST + "search/", data={"keyword": "let"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_keyword_min_length(self):
        response = self.client.get(
            self.URL_LIST + "search/", data={"keyword": "le"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("최소", response.data[0])

    def test_search_duplicate(self):
        seminar = baker.make(Seminar)
        track = baker.make(Track, seminar=seminar)
        baker.make(Session, name="SameName", track=track, _quantity=30)
        response = self.client.get(
            self.URL_LIST + "search/", data={"keyword": "same"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class SpeakerAPITest(APITestCase):
    URL_LIST = "/v1/seminars/speakers/"

    def test_list(self):
        baker.make(Speaker, _quantity=10)
        response = self.client.get(self.URL_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)

    def test_filter(self):
        seminars = baker.make(Seminar, _quantity=10)
        # 1세미나당 2개 트랙
        tracks = baker.make(Track, seminar=cycle(seminars), _quantity=20)

        # 1트랙당 5개 세션 (1세미나당 10개 세션)
        # 1세션당 1개 발표자 (1세미나당 10발표자)
        speakers = baker.make(Speaker, _quantity=100)
        baker.make(Session, track=cycle(tracks), speaker=cycle(speakers), _quantity=100)

        seminar = seminars[0]
        response = self.client.get(self.URL_LIST, data={"seminar": seminar.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)
        for data_speaker in response.data["results"]:
            self.assertIn(
                data_speaker["id"],
                list(
                    Speaker.objects.filter(
                        session_set__track__seminar_id=seminar.id
                    ).values_list("id", flat=True)
                ),
            )
