from django.core import mail
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APITestCase

from members.models import User, EmailVerification


class MembersScenarioTest(APITestCase):
    URL_EMAIL_VERIFICATION = "/v1/auth/email-verification/"
    URL_SIGNUP = "/v1/members/users/"

    def _get_email_verification_code(self, type, email):
        self.client.post(
            self.URL_EMAIL_VERIFICATION,
            data={"type": type, "email": email},
        )
        code = mail.outbox[0].body
        return code

    def test_signup_by_email(self):
        # 이메일 인증
        email = "sample@sample.com"
        code = self._get_email_verification_code(EmailVerification.TYPE_SIGNUP, email)

        # 회원가입
        response = self.client.post(
            self.URL_SIGNUP,
            data={
                "type": User.TYPE_EMAIL,
                "email_verification_code": code,
                "email": email,
                "nickname": "Sample Nickname",
                "password1": "SamplePassword",
                "password2": "SamplePassword",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 회원정보 확인
        user = User.objects.get(id=response.data["id"])
        self.assertEqual(user.username, email)
        self.assertEqual(user.email, email)
        self.assertEqual(user.email_verification.code, code)

    def test_signup_by_social(self):
        # 이메일 인증
        email = "sample@sample.com"
        uid = get_random_string(length=20)

        # 회원가입
        response = self.client.post(
            self.URL_SIGNUP,
            data={
                "type": User.TYPE_APPLE,
                "email": email,
                "uid": uid,
                "nickname": "Sample Nickname",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 회원정보 확인
        user = User.objects.get(id=response.data["id"])
        self.assertEqual(user.username, uid)
        self.assertEqual(user.email, email)
        self.assertFalse(hasattr(user, "email_verification"))
