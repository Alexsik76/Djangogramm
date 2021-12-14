from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
import logging
from cloudinary.models import CloudinaryField
import cloudinary.api
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
    avatar = CloudinaryField('image', blank=False, folder='django_gramm/avatars')
    objects = DjGrammUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def delete_media(self):
        cloudinary.api.delete_resources([self.avatar])

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


class Following(models.Model):
    follower_user = models.ForeignKey(DjGrammUser, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(DjGrammUser, related_name="followers", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower_user', 'following_user'], name='unique_follow'),
        ]

    def __str__(self):
        return f"{self.follower_user.get_full_name()} following {self.following_user.get_full_name()}"

    def save(self, *args, **kwargs):
        if self.follower_user == self.following_user:
            raise ValidationError('You can`t following yourself.')
        super().save(*args, **kwargs)

    @classmethod
    def follow(cls, following_user, follower_user):
        cls.objects.create(following_user=following_user, follower_user=follower_user)

    def unfollow(self):
        self.delete()
