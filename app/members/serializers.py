from django.conf import settings
from rest_auth.serializers import TokenSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from utils.drf.exceptions import (
    EmailVerificationDoesNotExist,
    EmailVerificationCodeInvalid,
)
from .models import User, EmailVerification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "type",
            "name",
            "nickname",
            "email",
            "phone_number",
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        try:
            ret["phone_number"] = instance.phone_number.as_national
        except AttributeError:
            pass
        return ret


class UserCreateSerializer(serializers.ModelSerializer):
    email_verification_code = serializers.CharField(help_text="이메일 인증코드")
    password1 = serializers.CharField(help_text="비밀번호")
    password2 = serializers.CharField(help_text="비밀번호 확인")

    class Meta:
        model = User
        fields = (
            "type",
            "name",
            "nickname",
            "email",
            "phone_number",
            "email_verification_code",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise ValidationError({"password2": "비밀번호와 비밀번호 확인란의 값이 다릅니다"})
        try:
            email_verification = EmailVerification.objects.get(
                email=data.get("email", "")
            )
            if email_verification.code != data["email_verification_code"]:
                raise EmailVerificationCodeInvalid(
                    {"email_verification_code": "이메일 인증코드가 유효하지 않습니다"}
                )
        except EmailVerification.DoesNotExist:
            raise EmailVerificationDoesNotExist(
                {"email_verification_code": "이메일 인증정보가 존재하지 않습니다"}
            )

        data["password"] = data["password2"]
        del data["password1"]
        del data["password2"]
        return data

    def create(self, validated_data):
        code = validated_data.pop("email_verification_code")
        user = self.Meta.model._default_manager.create_user(**validated_data)
        e = EmailVerification.objects.get(code=code)
        e.user = user
        e.save()
        return user

    def to_representation(self, instance):
        return UserSerializer(instance).data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "nickname",
            "email",
            "phone_number",
        )

    def to_representation(self, instance):
        return UserSerializer(instance).data


class UserAttributeAvailableSerializer(serializers.Serializer):
    attribute_name = serializers.CharField()
    value = serializers.CharField()


class AuthTokenSerializer(TokenSerializer):
    user = UserSerializer()

    class Meta(TokenSerializer.Meta):
        fields = TokenSerializer.Meta.fields + ("user",)


class EmailVerificationCheckSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, data):
        email = data["email"]
        code = data["code"]
        get_object_or_404(EmailVerification, email=email, code=code)
        return data


class EmailVerificationCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = EmailVerification
        fields = ("email",)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError(f'"{value}"은(는) 이미 사용중인 이메일입니다')
        return value

    def to_representation(self, instance):
        if settings.DEBUG:
            return EmailVerificationCheckSerializer(instance).data
        return super().to_representation(instance)
