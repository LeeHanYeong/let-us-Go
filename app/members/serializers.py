from django.conf import settings
from rest_auth.serializers import TokenSerializer, LoginSerializer
from rest_framework import serializers, status

from utils.drf import errors
from utils.drf.exceptions import ValidationError, APIException
from .models import User, EmailVerification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'type',
            'nickname',
            'email',
            'phone_number',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        try:
            ret['phone_number'] = instance.phone_number.as_national
        except AttributeError:
            pass
        return ret


class UserCreateSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(help_text='비밀번호')
    password2 = serializers.CharField(help_text='비밀번호 확인')

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'type',
            'nickname',
            'email',
            'phone_number',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False

    def validate(self, data):
        if not data.get('nickname'):
            raise ValidationError({'nickname': '닉네임은 필수항목입니다'})
        if data['password1'] != data['password2']:
            raise ValidationError({'password2': '비밀번호와 비밀번호 확인란의 값이 다릅니다'})
        try:
            email_verification = EmailVerification.objects.get(email=data.get('email', ''))
            if not email_verification.is_verification_completed:
                if not email_verification.is_send_succeed:
                    raise ValidationError(errors.EMAIL_SEND_FAILED_MSG, errors.EMAIL_SEND_FAILED)
                else:
                    raise ValidationError(errors.EMAIL_VERIFICATION_INCOMPLETED_MSG, errors.EMAIL_VERIFICATION_INCOMPLETED)

        except EmailVerification.DoesNotExist:
            raise ValidationError(errors.EMAIL_VERIFICATION_NOT_EXISTS_MSG, errors.EMAIL_VERIFICATION_NOT_EXISTS)

        data['password'] = data['password2']
        del data['password1']
        del data['password2']
        return data

    def create(self, validated_data):
        return self.Meta.model._default_manager.create_user(**validated_data)

    def to_representation(self, instance):
        return UserSerializer(instance).data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'nickname',
            'email',
            'phone_number',
        )

    def to_representation(self, instance):
        return UserSerializer(instance).data


class UserAttributeAvailableSerializer(serializers.Serializer):
    attribute_name = serializers.CharField()
    value = serializers.CharField()


class AuthTokenSerializer(TokenSerializer):
    user = UserSerializer()

    class Meta(TokenSerializer.Meta):
        fields = TokenSerializer.Meta.fields + (
            'user',
        )


class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = (
            'pk',
            'user',
            'email',
            'code',
        )


class EmailVerificationCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = EmailVerification
        fields = (
            'email',
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError(f'"{value}"은(는) 이미 사용중인 이메일입니다')
        return value

    def to_representation(self, instance):
        if settings.DEBUG:
            return EmailVerificationSerializer(instance).data
        return super().to_representation(instance)
