from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('Kullanıcı Adı'),
        max_length=30,
        unique=True,
        validators=[username_validator],
        help_text=_('30 karakter veya daha az, Türkçe olmayan, harf ve rakamlardan bir kelime.'),
    )
    first_name = models.CharField(_('Ad'), max_length=80)
    last_name = models.CharField(_('Soyad'), max_length=80)
    email = models.EmailField(_('E-Posta'))
    mobile = models.CharField(_('Cep Telefonu'), max_length=15, null=True, blank=True)
    photo = models.ImageField(upload_to='profile_photos/')
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(
        _('Kullanıcı etkin mi ?'),
        default=True,
        help_text=_('Bu kullanıcının etkin olarak işlem görüp görmediğini belirler. '
                    'Hesapları silmek yerine bunun işaretini kaldırın.')
    )
    user_permission = models.CharField(
        _('Kullanıcı Yetki'),
        max_length=20,
        choices=(
            ('superuser', _('Süper Yönetici')),
            ('api_user', _('API Kullanıcısı')),
            ('manager', _('Yönetici')),
            ('member', _('Normal Üye')),
        ),
        default='member',
        help_text=_('Kullanıcının sitedeki erişim sınırını belirler.')
    )
    last_login = models.DateTimeField(
        _('Son Oturum Açma'),
        null=True,
        blank=True,
        help_text=_('Kullanıcının en son sistemde oturum açma tarihi.')
    )
    date_joined = models.DateTimeField(
        _('Kayıt Tarihi'),
        auto_now_add=True,
        help_text=_('Kullanıcının sisteme kayıt tarihi.')
    )
    deleted_at = models.DateTimeField(_('Silinme Tarihi'), null=True, blank=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    # Gerekli metodlar
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    @property
    def is_superuser(self):
        return True if self.user_permission == 'superuser' else False

    @property
    def is_staff(self):
        return True if self.user_permission == 'superuser' else False

    @property
    def is_manager(self):
        return True if self.user_permission == 'manager' else False

    @property
    def is_member(self):
        return True if self.user_permission == 'member' else False

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} ( {self.username} )"
        return self.username

    class Meta:
        verbose_name = _('Kullanıcı')
        verbose_name_plural = _('Kullanıcılar')
        ordering = ('id',)
        db_table = 'users'
