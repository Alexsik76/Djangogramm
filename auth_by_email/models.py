from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Permission
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
        except (AttributeError, ValueError, FileNotFoundError) as e:
            logger.info(e)

    def delete(self, using=None, keep_parents=False):
        self.delete_media()
        return super().delete()

    def grant_user_permissions(self):
        all_perms_codename = ['view_post',
                              'delete_post',
                              'change_post',
                              'add_post']
        required_perms = [Permission.objects.get(codename=perms_codename) for perms_codename in all_perms_codename]
        self.user_permissions.set(required_perms)


class Follow(models.Model):
    """
    Followers are the users that follow you.
    Following the list of users that you follow.
    """
    follower = models.ForeignKey(DjGrammUser,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 related_name="followers")
    following = models.ForeignKey(DjGrammUser,
                                  on_delete=models.CASCADE,
                                  null=True,
                                  related_name="following")

    def __str__(self):
        return f"{self.follower.email} following {self.following.email} "
