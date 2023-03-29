

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    title = models.CharField(max_length=70, verbose_name=_('Titulo'))
    sub_title = models.CharField(
        max_length=250, default='', verbose_name=_('Subtitulo'))
    text = models.TextField(verbose_name=_('Texto'))
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cover = models.ImageField(
        upload_to='post/cover/%Y-%m-%d/', blank="True", default='',
        verbose_name=_('Imagem'))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
