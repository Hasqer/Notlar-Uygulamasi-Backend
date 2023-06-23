from django_filters import rest_framework as filters
from notebooks import models


class TasksFilter(filters.FilterSet):
    no_group = filters.BooleanFilter(field_name='task_group', lookup_expr='isnull')
    no_assigned = filters.BooleanFilter(field_name='assigned_to', lookup_expr='isnull')

    # assigned_me = filters.BooleanFilter(method='filter_assigned_me')
    #
    # def filter_assigned_me(self, queryset, name, value):
    #     if value:
    #         return queryset.filter(notebook__users=self.request.user, assigned_to=self.request.user)
    #     else:
    #         return queryset.filter(notebook__users=self.request.user)

    class Meta:
        model = models.Tasks
        fields = ("task_group", "notebook", "status", "assigned_to")


class NotesFilter(filters.FilterSet):
    class Meta:
        model = models.Notes
        fields = ("notebook",)


class TaskGroupFilter(filters.FilterSet):
    class Meta:
        model = models.TaskGroup
        fields = ("notebook",)
