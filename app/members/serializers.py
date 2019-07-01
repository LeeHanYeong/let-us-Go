from django.conf import settings
from rest_auth.serializers import TokenSerializer, LoginSerializer
from rest_framework import serializers

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
            raise serializers.ValidationError({'nickname': '닉네임은 필수항목입니다'})
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호와 비밀번호확인란의 값이 다릅니다')
        try:
            email_verification = EmailVerification.objects.get(email=data.get('email', ''))
            if not email_verification.is_verification_completed:
                if not email_verification.is_send_succeed:
                    raise serializers.ValidationError('인증 이메일 발송에 실패했습니다.')
                else:
                    raise serializers.ValidationError('이메일 인증이 완료되지 않았습니다. 메일을 확인해주세요')

        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError('이메일 인증정보가 없습니다')

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
            raise serializers.ValidationError(f'"{value}"은(는) 이미 사용중인 이메일입니다')
        return value

    def to_representation(self, instance):
        if settings.DEBUG:
            return EmailVerificationSerializer(instance).data
        return super().to_representation(instance)
