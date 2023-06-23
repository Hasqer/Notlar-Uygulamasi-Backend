from django.utils.translation import gettext_lazy as _

ERROR_MESSAGE = _('Hata oluştu, lütfen daha sonra tekrar deneyiniz.')
SUCCESS_MESSAGE = _('İşlem başarıyla gerçekleştirildi.')

NOTE = {
    'tags': ['Notebooks - Note - Member'],
    'list_desc': 'ordering: title, created_at, updated_at'
}

NOTEBOOK = {
    'tags': ['Notebooks - Notebook - Member'],
    'list_desc': 'ordering: title, created_at, updated_at'
}

TASK = {
    'tags': ['Notebooks - Task - Member'],
    'list_desc': 'ordering: title, rank, created_at, updated_at'
}

TASK_GROUP = {
    'tags': ['Notebooks - Task Group - Member'],
    'list_desc': 'ordering: title, created_at, updated_at'
}
