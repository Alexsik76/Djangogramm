import logging
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from auth_by_email.models import DjGrammUser

# Create your models here.

logger = logging.getLogger(__name__)


class PostQuerySet(models.QuerySet):
    def delete(self):
        for item in self:
            item.delete_media()
        return super().delete()


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(model=self.model, using=self._db, hints=self._hints)


class Post(models.Model):
    title = models.CharField(_('Title'), max_length=256, blank=False)
    image = models.ImageField(upload_to='pasts_images')
    author = models.ForeignKey(DjGrammUser,
                               on_delete=models.CASCADE,
                               null=True)
    objects = PostManager()

    def delete_media(self):
        try:
            file_name = settings.BASE_DIR / self.image.file.name
            if file_name.exists():
                self.image.file.close()
                file_name.unlink()
        except (AttributeError, ValueError, FileNotFoundError) as e:
            logger.info(e)

    def delete(self, using=None, keep_parents=False):
        self.delete_media()
        return super().delete()


class Like(models.Model):
    liker = models.ForeignKey(DjGrammUser,
                              on_delete=models.CASCADE,
                              null=True,
                              related_name='liker')
    liked = models.ForeignKey(Post,
                              on_delete=models.CASCADE,
                              null=True,
                              related_name='liked')
