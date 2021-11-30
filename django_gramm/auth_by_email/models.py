from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import logging
# Create your models here.

logger = logging.getLogger(__name__)


class MyQuerySet(models.QuerySet):
    def delete(self):
        for item in self:
            item.delete_media()
        return super().delete()


class DjGrammUserManager(BaseUserManager):

    def get_queryset(self):
        return MyQuerySet(model=self.model, using=self._db, hints=self._hints)

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class DjGrammUser(AbstractUser):
    BIO_CHOICES = [(None, _('select gender')), (_('Mr'), _('mister')), (_('Mrs'), _('misses'))]
    username = None
    email = models.EmailField(_('email address'), blank=False, unique=True)
    bio = models.CharField(_('bio'), max_length=3, blank=False, choices=BIO_CHOICES)
    avatar = models.ImageField(upload_to='auth_by_email/users_avatars')
    objects = DjGrammUserManager()

    class Meta:
        permissions = [('gramm_app.create_post', 'Can create post'),
                       ('gramm_app.edit_post', 'Can change post'),
                       ('gramm_app.view_post', 'Can view post'),
                       ('gramm_app.delete_post', 'Can delete post'),
                       ('gramm_app.view_posts', 'Can view all posts')
                       ]

    REQUIRED_FIELDS = ['bio', 'avatar']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def delete_media(self):
        try:
            file_name = settings.BASE_DIR / self.avatar.file.name
            if file_name.exists():
                self.avatar.file.close()
                file_name.unlink()
        except (AttributeError, ValueError) as e:
            logger.info(e)

    def delete(self, using=None, keep_parents=False):
        self.delete_media()
        return super().delete()
