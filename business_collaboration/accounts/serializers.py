from rest_framework_simplejwt.exceptions import TokenError
from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import authenticate
from datetime import datetime
from HR.models import Personal


class CompanySerializer(serializers.ModelSerializer): # Регистрация для директора
    class Meta:
        model = UserProfile
        fields = ('name_company', 'registration_number_company', 'address_company', 'industry', 'full_name', 'email',
                  'password', 'position',
                  'phone_number',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['role'] = 'Administrator'
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        access_token_expiration = datetime.fromtimestamp(refresh.access_token['exp']).isoformat()
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'access_token_expiration': access_token_expiration,
        }


class CompanyLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        access_token_expiration = datetime.fromtimestamp(refresh.access_token['exp']).isoformat()
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'access_token_expiration': access_token_expiration,
        }


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get('refresh_token')
        if not refresh_token:
            raise serializers.ValidationError('Refresh токен не предоставлен.')
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as e:
            raise serializers.ValidationError('Недействительный токен.')

        return attrs


class UserSerializer(serializers.ModelSerializer): # Регистрация для обычных пользователей
    class Meta:
        model = UserSimple
        fields = ('full_name', 'email', 'password',
                  'phone_number',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['role'] = 'User'
        user = UserSimple.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        access_token_expiration = datetime.fromtimestamp(refresh.access_token['exp']).isoformat()
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'access_token_expiration': access_token_expiration,
        }


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        access_token_expiration = datetime.fromtimestamp(refresh.access_token['exp']).isoformat()
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'access_token_expiration': access_token_expiration,
        }


class EmployeeLoginSerializer(serializers.Serializer): # Login для сотрудников компании
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user and user.is_active:
            if Personal.objects.filter(employee=user).exists():
                return user
            raise serializers.ValidationError('Сотрудник не найден')
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        access_token_expiration = datetime.fromtimestamp(refresh.access_token['exp']).isoformat()
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'access_token_expiration': access_token_expiration,
        }


# ---------------------------------------


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name_company', 'registration_number_company', 'address_company', 'industry', 'full_name', 'email',
                  'password', 'position',
                  'phone_number',]


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserSimple
        fields = ['full_name', 'image_user', 'phone_number', 'email']


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']


class OpeningsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Openings
        fields = ['opening_name', 'description']


class OpeningsTwoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Openings
        fields = ['opening_name', 'description']


class OpeningsSreeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Openings
        fields = ['opening_name', 'description']