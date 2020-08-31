from django.conf import settings
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from utils.drf.exceptions import (
    EmailVerificationDoesNotExist,
    EmailVerificationCodeInvalid,
    InvalidCredentials,
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
        self.fields["type"].required = True

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
        with transaction.atomic():
            code = validated_data.pop("email_verification_code")
            user = User.objects.create_user(**validated_data)
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


class UserPasswordResetRequestSerializer(serializers.ModelSerializer):
    type = serializers.HiddenField(default=EmailVerification.TYPE_PASSWORD_RESET)

    class Meta:
        model = EmailVerification
        fields = ("type", "email")


class UserPasswordResetSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        code = data["code"]
        email = data["email"]
        get_object_or_404(
            EmailVerification,
            type=EmailVerification.TYPE_PASSWORD_RESET,
            email=email,
            code=code,
        )
        data["user"] = get_object_or_404(User, email=email)
        return data


class AuthTokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Token
        fields = (
            "key",
            "user",
        )


class GetEmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            msg = "이메일 또는 비밀번호를 확인해주세요"
            raise InvalidCredentials(msg)
        attrs["user"] = user
        return attrs


class EmailVerificationCheckSerializer(serializers.Serializer):
    type = serializers.HiddenField(default=EmailVerification.TYPE_SIGNUP)
    email = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, data):
        email = data["email"]
        code = data["code"]
        get_object_or_404(
            EmailVerification,
            type=EmailVerification.TYPE_SIGNUP,
            email=email,
            code=code,
        )
        return data


class EmailVerificationCreateSerializer(serializers.ModelSerializer):
    type = serializers.HiddenField(default=EmailVerification.TYPE_SIGNUP)
    email = serializers.EmailField(required=True)

    class Meta:
        model = EmailVerification
        fields = (
            "type",
            "email",
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError(f'"{value}"은(는) 이미 사용중인 이메일입니다')
        return value

    def to_representation(self, instance):
        if settings.LOCAL:
            return EmailVerificationCheckSerializer(instance).data
        return super().to_representation(instance)
