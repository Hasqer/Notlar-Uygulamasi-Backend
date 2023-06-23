from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
from accounts.permissions import IsManager, IsMember
from rest_framework.generics import get_object_or_404
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, WriteUserProfileSerializer, \
    ReadUserProfileSerializer


@extend_schema(
    tags=['Accounts - Users - Manager']
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsManager)
    pagination_class = None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        for data in serializer.data:
            data['full_name'] = f"{data['first_name']} {data['last_name']}"
        return Response(serializer.data)


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = []
    "permission_classes = [AllowAny]"

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': _('Kayıt işleminiz başarıyla gerçekleşti.')},
            status=status.HTTP_201_CREATED
        )


@extend_schema(
    tags=['Accounts - Users - Member']
)
class UserProfileView(APIView):
    permission_classes = (IsAuthenticated, IsMember)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='email',
                type=str,
                location=OpenApiParameter.QUERY
            )
        ]
    )
    def get(self, request):
        email = request.query_params.get('email')
        user = self.get_user(email)
        serializer = ReadUserProfileSerializer(user)
        return Response(serializer.data)

    @extend_schema(
        request=WriteUserProfileSerializer,
        responses=WriteUserProfileSerializer
    )
    def patch(self, request):
        serializer = WriteUserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def get_user(self, email):
        if email:
            queryset = get_object_or_404(User, email=email)
        else:
            queryset = get_object_or_404(User, email=self.request.user.email)

        return queryset
