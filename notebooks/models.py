from django.db import models
from accounts.models import User
from ornekproje import models as app_models
from django.utils.translation import gettext_lazy as _


class Notebook(app_models.BaseModel):
    users = models.ManyToManyField(User, related_name='notebook')
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title or str(self.id)

    class Meta:
        ordering = ['id']
        verbose_name = _('Not defteri')
        verbose_name_plural = _('Not defterleri')


class Notes(app_models.BaseModel):
    creator = models.ForeignKey(User, related_name='creator_notes', on_delete=models.CASCADE)
    notebook = models.ForeignKey(Notebook, related_name='notes', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title or str(self.id)

    class Meta:
        ordering = ['id']
        verbose_name = _('Not')
        verbose_name_plural = _('Notlar')


class TaskGroup(app_models.BaseModel):
    notebook = models.ForeignKey(Notebook, related_name='task_group', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title or str(self.id)

    class Meta:
        ordering = ['id']
        verbose_name = _('Görev grubu')
        verbose_name_plural = _('Görev grupları')


class Tasks(app_models.BaseModel):
    notebook = models.ForeignKey(Notebook, related_name='notebook_tasks', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='creator_tasks', on_delete=models.CASCADE)
    task_group = models.ForeignKey(TaskGroup, related_name='tasks', on_delete=models.RESTRICT, null=True, blank=True)
    assigned_to = models.ForeignKey(User, related_name='assigned_to_tasks', on_delete=models.CASCADE,
                                    null=True, blank=True, verbose_name=_("Atanacak kullanıcı"))

    status = models.BooleanField(default=False)
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    rank = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title or str(self.id)

    class Meta:
        ordering = ['rank']
        verbose_name = _('Görev')
        verbose_name_plural = _('Görevler')
