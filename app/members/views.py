from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import EmailVerification


class EmailValidationView(View):
    def get(self, request, code):
        try:
            validation_obj = EmailVerification.objects.get(code=code)
        except EmailVerification.DoesNotExist:
            return HttpResponse("유효하지 않은 인증코드입니다")

        validation_obj.status_verification = EmailVerification.SUCCEED
        validation_obj.save()
        return HttpResponse(f"이메일({validation_obj.email})의 인증이 완료되었습니다. 회원가입을 진행해주세요")
