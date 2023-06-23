from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import inline_serializer


def custom_response(name: str, message: str, field_type: str = 'str'):
    if field_type == 'boolean':
        return inline_serializer(
            name, fields={'detail': serializers.BooleanField(default=message)}
        )
    return inline_serializer(
        name, fields={'detail': serializers.CharField(default=message)}
    )


class SuccessResponse(serializers.Serializer):
    detail = serializers.CharField(default=_('Başarılı.'))

    def create(self, validated_data):
        return SuccessResponse(**validated_data)

    def update(self, instance, validated_data):
        return SuccessResponse(**validated_data)
