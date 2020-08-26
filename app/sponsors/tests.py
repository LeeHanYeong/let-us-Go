from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from seminars.models import Seminar
from sponsors.models import SponsorTier, Sponsor


class SponsorTierAPITest(APITestCase):
    URL_LIST = "/v1/sponsors/tiers/"

    def test_list(self):
        seminar = baker.make(Seminar)
        tier = baker.make(SponsorTier, seminar=seminar)
        baker.make(Sponsor, tier=tier, _quantity=10)
        response = self.client.get(self.URL_LIST, data={"seminar": seminar.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
