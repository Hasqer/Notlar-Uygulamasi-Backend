from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import NotebookViewSet, NotesViewSet, TasksViewSet, TaskGroupViewSet

router = DefaultRouter()
router.register('list', NotebookViewSet, basename='notebook')
router.register('notes', NotesViewSet, basename='notes')
router.register('tasks', TasksViewSet, basename='notes')
router.register('task-group', TaskGroupViewSet, basename='notes')

urlpatterns = [
    path('', include(router.urls)),
]
