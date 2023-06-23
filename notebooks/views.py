from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, AllowAny
from rest_framework.response import Response
from accounts.permissions import IsMember
from notebooks import doc_tags, filters
from rest_framework.decorators import action
from ornekproje import responses

from .models import Notebook, Tasks, TaskGroup, Notes
from notebooks import serializers


#
# @extend_schema(
#     tags=['Movie'],
#     description='Ordering: bla bla'
# )
# class MovieViewSet(viewsets.ModelViewSet):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#
#     # permission_classes = (IsAuthenticated, IsMember)
#     search_fields = (
#         'title',
#     )
#     ordering_fields = (
#         '__all__'
#     )
#
#     @extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 name='araba_marka',
#                 type=str,
#                 location=OpenApiParameter.QUERY,
#                 description='Araba markası'
#             )
#         ]
#     )
#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)
#
#     def create(self, request, *args, **kwargs):
#         return super().create(request, *args, **kwargs)

#
# @extend_schema(
#     tags=['Test endpoint \'i'],
#     description='Ordering: bla bla',
# )
# class UserGetDataView(APIView):
#     def get(self, request):
#         user = request.user
#         print("Kullanıcı adı:", user.username)
#         print("Adı:", user.first_name)
#         print("Soyadı:", user.last_name)
#         print("E-posta:", user.email)
#         print("Sifre:", user.password)
#         return Response({"test": "tesst"}, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(tags=doc_tags.NOTEBOOK['tags'], description=doc_tags.NOTEBOOK['list_desc']),
    create=extend_schema(tags=doc_tags.NOTEBOOK['tags']),
    retrieve=extend_schema(tags=doc_tags.NOTEBOOK['tags'], responses=serializers.ReadDetailNotebookSerializer),
    update=extend_schema(tags=doc_tags.NOTEBOOK['tags']),
    partial_update=extend_schema(tags=doc_tags.NOTEBOOK['tags']),
    destroy=extend_schema(tags=doc_tags.NOTEBOOK['tags']),
    add_user=extend_schema(
        tags=doc_tags.NOTEBOOK['tags'],
        request=serializers.AddUserNotebooksSerializer,
        responses={
            200: responses.SuccessResponse
        }
    ),
    remove_user=extend_schema(
        tags=doc_tags.NOTEBOOK['tags'],
        request=serializers.RemoveUserNotebooksSerializer,
        responses={
            200: responses.SuccessResponse
        }
    ),
)
class NotebookViewSet(viewsets.ModelViewSet):
    queryset = Notebook.objects.all()
    serializer_class = serializers.ReadNotebookSerializer
    permission_classes = (IsAuthenticated, IsMember)
    pagination_class = None
    search_fields = (
        'title',
    )
    ordering_fields = (
        'title', 'created_at', 'updated_at'
    )

    def get_queryset(self):
        self.queryset = self.queryset.filter(users=self.request.user)
        return self.queryset

    def retrieve(self, request, *args, **kwargs):
        self.queryset = Notebook.objects. \
            prefetch_related('users')
        self.serializer_class = serializers.ReadDetailNotebookSerializer
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        instance = serializer.save()
        user = self.request.user
        instance.users.add(user)

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            self.serializer_class = serializers.WriteNotebookSerializer
        return self.serializer_class

    @action(methods=['POST'], detail=False, url_path='add-user')
    def add_user(self, request, *args, **kwargs):
        serializer = serializers.AddUserNotebooksSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        notebook = serializer.validated_data['notebook']
        user = serializer.validated_data['user']

        notebook.users.add(user)
        notebook.save()
        return Response({'detail': doc_tags.SUCCESS_MESSAGE}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, url_path='remove-user')
    def remove_user(self, request, *args, **kwargs):
        serializer = serializers.RemoveUserNotebooksSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        notebook = serializer.validated_data['notebook']
        user = serializer.validated_data['user']

        notebook.users.remove(user)
        notebook.save()
        return Response({'detail': doc_tags.SUCCESS_MESSAGE}, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(tags=doc_tags.NOTE['tags'], description=doc_tags.NOTE['list_desc']),
    create=extend_schema(tags=doc_tags.NOTE['tags']),
    retrieve=extend_schema(tags=doc_tags.NOTE['tags']),
    update=extend_schema(tags=doc_tags.NOTE['tags']),
    partial_update=extend_schema(tags=doc_tags.NOTE['tags']),
    destroy=extend_schema(tags=doc_tags.NOTE['tags']),
)
class NotesViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = serializers.ReadNotesSerializer
    permission_classes = (IsAuthenticated, IsMember)
    filterset_class = filters.NotesFilter
    pagination_class = None
    search_fields = (
        'title',
    )
    ordering_fields = (
        'title', 'created_at', 'updated_at'
    )

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = serializers.ReadDetailNotesSerializer
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            self.serializer_class = serializers.WriteNotesSerializer
        return self.serializer_class


@extend_schema_view(
    list=extend_schema(
        tags=doc_tags.TASK['tags'],
        description=doc_tags.TASK['list_desc']
        #        ,parameters=[
        #     OpenApiParameter(
        #         name='assigned_me',
        #         type=bool,
        #         location=OpenApiParameter.QUERY
        #     )
        # ]
    ),
    create=extend_schema(tags=doc_tags.TASK['tags']),
    retrieve=extend_schema(tags=doc_tags.TASK['tags']),
    update=extend_schema(tags=doc_tags.TASK['tags']),
    partial_update=extend_schema(tags=doc_tags.TASK['tags']),
    destroy=extend_schema(tags=doc_tags.TASK['tags']),
    change_rank=extend_schema(
        tags=doc_tags.TASK['tags'],
        request=serializers.ChangeRankTasksSerializer,
        responses={
            200: responses.SuccessResponse
        }
    )
)
class TasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.select_related('assigned_to').select_related('creator')
    serializer_class = serializers.ReadTasksSerializer
    filterset_class = filters.TasksFilter
    permission_classes = (IsAuthenticated, IsMember)
    pagination_class = None
    search_fields = (
        'title',
    )
    ordering_fields = (
        'title', 'rank', 'created_at', 'updated_at'
    )

    def get_queryset(self):
        self.queryset = self.queryset.filter(notebook__users=self.request.user)
        return self.queryset

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            self.serializer_class = serializers.WriteTasksSerializer
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        if self.request.method == 'PATCH':
            serializer.fields.pop('rank', None)
        return serializer

    def perform_create(self, serializer):
        start_rank = serializer.validated_data['rank']
        notebook = serializer.validated_data['notebook']
        instance = serializer.save()
        filter_dict = {
            'rank__gte': start_rank,
            "notebook": notebook
        }
        update_qs = Tasks.objects.exclude(id=instance.id).filter(**filter_dict).order_by('rank')
        for obj in update_qs:
            start_rank += 1
            obj.rank = start_rank
            obj.save()

        if start_rank is not None:
            return Response({'detail': doc_tags.SUCCESS_MESSAGE}, status=status.HTTP_200_OK)

        last = Tasks.objects.filter(notebook=serializer.validated_data['notebook']).last()
        if last:
            rank = last.rank + 1
        else:
            rank = 1
        serializer.save(rank=rank)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        filtered_queryset = self.filterset_class(request.GET, queryset=queryset).qs

        true_count = filtered_queryset.filter(status=True).count()
        false_count = filtered_queryset.filter(status=False).count()

        serializer = self.get_serializer(filtered_queryset, many=True)
        response_data = {
            'all_count': true_count + false_count,
            'true_count': true_count,
            'false_count': false_count,
            'tasks': serializer.data
        }
        return Response(response_data)

    @action(methods=['POST'], detail=False, url_path='change-rank')
    def change_rank(self, request, *args, **kwargs):
        serializer = serializers.ChangeRankTasksSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        task = serializer.validated_data['task']
        old_rank = task.rank
        new_rank = serializer.validated_data['new_rank']

        task.rank = new_rank
        task.save()
        if old_rank > new_rank:
            rank_start = new_rank
            filter_dict = {
                'rank__gte': new_rank,
                'rank__lte': old_rank,
                'notebook': task.notebook
            }
        else:
            rank_start = old_rank
            filter_dict = {
                'rank__gte': old_rank,
                'rank__lte': new_rank,
                'notebook': task.notebook
            }
        update_qs = Tasks.objects.exclude(id=task.id).filter(**filter_dict).order_by('rank')
        for obj in update_qs:
            obj.rank = rank_start
            obj.save()
            rank_start += 1

        return Response({'detail': doc_tags.SUCCESS_MESSAGE}, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(tags=doc_tags.TASK_GROUP['tags'], description=doc_tags.TASK_GROUP['list_desc']),
    create=extend_schema(tags=doc_tags.TASK_GROUP['tags']),
    retrieve=extend_schema(tags=doc_tags.TASK_GROUP['tags']),
    update=extend_schema(tags=doc_tags.TASK_GROUP['tags']),
    partial_update=extend_schema(tags=doc_tags.TASK_GROUP['tags']),
    destroy=extend_schema(tags=doc_tags.TASK_GROUP['tags']),
)
class TaskGroupViewSet(viewsets.ModelViewSet):
    queryset = TaskGroup.objects.all()
    serializer_class = serializers.ReadTaskGroupSerializer
    pagination_class = None
    filterset_class = filters.TaskGroupFilter
    permission_classes = (IsAuthenticated, IsMember)
    search_fields = (
        'title',
    )
    ordering_fields = (
        'title', 'created_at', 'updated_at'
    )

    def get_queryset(self):
        self.queryset = self.queryset.filter(notebook__users=self.request.user)
        return self.queryset

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            self.serializer_class = serializers.WriteTaskGroupSerializer
        return self.serializer_class
