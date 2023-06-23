from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from accounts import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'mobile'
        )
        read_only_fields = (
            'id',
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=5,
        max_length=128,
        style={'input_type': 'password'},
        write_only=True,
        required=True,
        allow_null=False
    )
    email = serializers.EmailField(
        label=_('E-Posta'), required=True, allow_null=False,
        validators=[UniqueValidator(queryset=models.User.objects.all())]
    )
    mobile = serializers.CharField(
        label=_('Cep Telefonu'), allow_null=False,
        validators=[UniqueValidator(queryset=models.User.objects.all())]
    )

    class Meta:
        model = models.User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'mobile', 'password'
        )
        read_only_fields = (
            'id',
        )

    def create(self, validated_data):
        validated_data['user_permission'] = 'member'
        self.instance = models.User.objects.custom_create_user(**validated_data)
        return self.instance


class ReadUserProfileSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'mobile', 'photo'
        )
        read_only_fields = ('id',)

    def get_photo(self, obj):
        if obj.photo:
            return f"{settings.DOWNLOAD_DOMAIN}{obj.photo.url}"
        return None


class WriteUserProfileSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'mobile', 'photo'
        )
        read_only_fields = ('id',)

    def get_id(self, obj):
        return self.context['request'].user.id
