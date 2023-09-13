from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField
import cloudinary.api


# Create your models here.


class MyQuerySet(models.QuerySet):
    def delete(self):
        """
        Extended for delete users avatar after delete user. This needs because:
        "Keep in mind that this will, whenever possible,
        be executed purely in SQL, and so delete() methods of individual object
        instances will not necessarily be called during the process".
        """
        for item in self:
            item.delete_media()
        return super().delete()


class DjGrammUserManager(BaseUserManager):

    def get_queryset(self):
        return MyQuerySet(model=self.model, using=self._db, hints=self._hints)

    def _create_user(self, email, password, **extra_fields):
        """
        Creates user on stage signup or with createsuperuser command.
        Because has a minimal needed fields
        """
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, **fields):
        """
        Creates user on stage signup  with social-auth module.
        """
        if fields.get('email', None):
            password = 'password'
            email = fields['email']
            user = self._create_user(email, password)
            return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

    @classmethod
    def user_model(cls):
        return DjGrammUser


class DjGrammUser(AbstractUser):
    BIO_CHOICES = [(None, _('select gender')), (_('Mr'), _('mister')),
                   (_('Mrs'), _('misses'))]
    username = None
    email = models.EmailField(_('email address'), blank=False, unique=True)
    bio = models.CharField(_('bio'), max_length=3, blank=False,
                           choices=BIO_CHOICES)
    avatar = CloudinaryField('image', blank=False,
                             folder='django_gramm/avatars',
                             use_filename=True)
    objects = DjGrammUserManager()

    class Meta:
        app_label = 'auth_by_email'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def make_inactive_user(self):
        """Makes inactive user for the registration stage"""
        self.is_active = False
        self.set_unusable_password()
        self.username = self.email
        return self

    def delete_media(self):
        """For delete media when the user is deleted directly or in queryset"""
        cloudinary.api.delete_resources([self.avatar])

    def delete(self, using=None, keep_parents=False):
        """Also deletes avatar from cloudinary"""
        self.delete_media()
        return super().delete()

    def grant_user_permissions(self):
        """Grant standard permissions for the  most views"""
        all_perms_codename = ['view_post',
                              'delete_post',
                              'change_post',
                              'add_post']
        required_perms = [Permission.objects.get(codename=perms_codename) for
                          perms_codename in all_perms_codename]
        self.user_permissions.set(required_perms)

    def follow(self, another_user):
        """
        Creates Following object.
        In the case of another_user is followed, unfollow it
        """
        if another_user.is_followed(self):
            self.unfollow(another_user)
        else:
            Following.objects.create(following_user=another_user,
                                     follower_user=self)

    def unfollow(self, another_user):
        following = self.following.get(following_user_id=another_user.id)
        following.delete()

    def is_followed(self, another_user):
        return self.followers.filter(follower_user_id=another_user.id).exists()


class Following(models.Model):
    """
    Followers are the users that follow you.
    Following refers to the list of users that you follow.
    """
    follower_user = models.ForeignKey(DjGrammUser, related_name="following",
                                      on_delete=models.CASCADE)
    following_user = models.ForeignKey(DjGrammUser, related_name="followers",
                                       on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower_user.get_full_name()} follows " \
               f"{self.following_user.get_full_name()}"

    def save(self, *args, **kwargs):
        """Forbids to follow oneself"""
        if self.follower_user == self.following_user:
            raise ValidationError('You can`t following yourself.')
        super().save(*args, **kwargs)
