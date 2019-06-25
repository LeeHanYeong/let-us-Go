from rest_framework import serializers

from .models import User


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

    def validate(self, data):
        if not data.get('nickname'):
            raise serializers.ValidationError({'nickname': '닉네임은 필수항목입니다'})
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호와 비밀번호확인란의 값이 다릅니다')
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
