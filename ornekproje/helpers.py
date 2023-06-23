from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 200


def get_object_or_404_with_field(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        raise serializers.ValidationError(
            'Girilen değere erişim izniniz bulunmamaktadır.')  # The field you entered does not belong to you.
