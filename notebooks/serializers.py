from rest_framework import serializers

from accounts.serializers import ReadUserProfileSerializer
from notebooks import models
from ornekproje.helpers import get_object_or_404_with_field
from django.core.exceptions import ObjectDoesNotExist


# class MovieSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     class Meta:
#         model = models.Movie
#         fields = '__all__'


# Notes
class ReadNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notes
        fields = ('id', 'title', 'created_at', 'updated_at')
        read_only_fields = (
            'id', 'created_at', 'updated_at'
        )


class ReadDetailNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notes
        fields = ('id', 'content', 'created_at', 'updated_at')
        read_only_fields = (
            'id', 'created_at', 'updated_at'
        )


class WriteNotesSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_notebook(self, value):
        if value is None:
            return value
        get_object_or_404_with_field(models.Notebook, id=value.id, users=self.context['request'].user)
        return value

    class Meta:
        model = models.Notes
        fields = ('id', 'notebook', 'creator', 'title', 'content', 'created_at', 'updated_at')
        read_only_fields = (
            'id', 'creator', 'created_at', 'updated_at'
        )


class SubNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notes
        fields = ('id', 'title')
        read_only_fields = (
            'id',
        )


# Tasks
class ReadTasksSerializer(serializers.ModelSerializer):
    assigned_to = ReadUserProfileSerializer(default="")
    creator = ReadUserProfileSerializer(default="")

    class Meta:
        model = models.Tasks
        fields = (
            'id', 'title', 'description', 'assigned_to', 'status', 'task_group', 'creator', 'created_at', 'updated_at',
            'rank')
        read_only_fields = (
            'id', 'created_at', 'updated_at'
        )


class WriteTasksSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # assigned_to = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all())

    def validate_notebook(self, value):
        if value is None:
            return value
        get_object_or_404_with_field(models.Notebook, id=value.id, users=self.context['request'].user)
        return value

    def validate_assigned_to(self, value):
        if value is None:
            return value
        notebook_id = self.initial_data.get('notebook')
        try:
            models.Notebook.objects.get(id=notebook_id, users=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Bu kullanıcının not defterine erişimi yok')
        return value

    def validate_task_group(self, value):
        if value is None:
            return value
        get_object_or_404_with_field(models.TaskGroup, id=value.id, notebook__users=self.context['request'].user)
        return value

    class Meta:
        model = models.Tasks
        fields = (
            'id', 'creator', 'assigned_to', 'status', 'notebook', 'task_group', 'title', 'description', 'rank')
        read_only_fields = (
            'id', 'creator', 'created_at', 'updated_at'
        )


class SubTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tasks
        fields = ('id', 'title', 'status')
        read_only_fields = (
            'id',
        )


class ChangeRankTasksSerializer(serializers.Serializer):
    task = serializers.PrimaryKeyRelatedField(queryset=models.Tasks.objects.all())
    new_rank = serializers.IntegerField(min_value=0)

    def validate_task(self, value):
        if value is None:
            return value
        get_object_or_404_with_field(models.Tasks, id=value.id, notebook__users=self.context['request'].user)
        return value

    def create(self, validated_data):
        return ChangeRankTasksSerializer(**validated_data)

    def update(self, instance, validated_data):
        return ChangeRankTasksSerializer(**validated_data)


class AssignedMeTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tasks
        fields = ('id', 'title')
        read_only_fields = fields


# TaskGroup
class ReadTaskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskGroup
        fields = ('id', 'title')
        read_only_fields = (
            'id',
        )


class WriteTaskGroupSerializer(serializers.ModelSerializer):

    def validate_notebook(self, value):
        if value is None:
            return value
        get_object_or_404_with_field(models.Notebook, id=value.id, users=self.context['request'].user)
        return value

    class Meta:
        model = models.TaskGroup
        fields = ('id', 'title', 'notebook')
        read_only_fields = (
            'id',
        )


class SubTaskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskGroup
        fields = ('id', 'title')
        read_only_fields = (
            'id',
        )


# Notebook
class ReadNotebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notebook
        fields = (
            'id', 'title', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'created_at', 'updated_at'
        )


class ReadDetailNotebookSerializer(serializers.ModelSerializer):
    users = ReadUserProfileSerializer(many=True, default="")

    class Meta:
        model = models.Notebook
        fields = (
            'id', 'title', 'users', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'created_at', 'updated_at'
        )


class WriteNotebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notebook
        fields = ('id', 'title', 'created_at', 'updated_at')
        read_only_fields = (
            'id', 'created_at', 'updated_at'
        )


class AddUserNotebooksSerializer(serializers.Serializer):
    notebook = serializers.PrimaryKeyRelatedField(queryset=models.Notebook.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all())

    def validate_notebook(self, value):
        if value is None:
            return value
        get_object_or_404_with_field(models.Notebook, id=value.id, users=self.context['request'].user)
        return value

    def create(self, validated_data):
        return AddUserNotebooksSerializer(**validated_data)

    def update(self, instance, validated_data):
        return AddUserNotebooksSerializer(**validated_data)


class RemoveUserNotebooksSerializer(serializers.Serializer):
    notebook = serializers.PrimaryKeyRelatedField(queryset=models.Notebook.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all())

    def validate_notebook(self, value):
        if value is None:
            return value
        get_object_or_404_with_field(models.Notebook, id=value.id, users=self.context['request'].user)
        return value

    def create(self, validated_data):
        return RemoveUserNotebooksSerializer(**validated_data)

    def update(self, instance, validated_data):
        return RemoveUserNotebooksSerializer(**validated_data)
