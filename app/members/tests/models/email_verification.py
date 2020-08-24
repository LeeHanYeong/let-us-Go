from django.test import TestCase
from model_bakery import baker

from members.models import EmailVerification


class EmailVerificationManagerTest(TestCase):
    def test_create(self):
        EmailVerification.objects.create()
        self.assertEqual(EmailVerification.objects.count(), 1)

    def test_already_created_reset_code(self):
        e1 = baker.make(EmailVerification)
        e2 = EmailVerification.objects.create(email=e1.email)
        self.assertEqual(e1.id, e2.id)
        self.assertNotEqual(e1.code, e2.code)


class EmailVerificationModelTest(TestCase):
    def test_reset_code(self):
        e = baker.make(EmailVerification)
        origin_code = e.code
        e.reset_code()
        reset_code = e.code
        self.assertNotEqual(origin_code, reset_code)
