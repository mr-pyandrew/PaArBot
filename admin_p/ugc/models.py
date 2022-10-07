import datetime
import json

import pytz
from django.utils.timezone import now
from django.db import models
from tinymce.models import HTMLField


class Users(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='ID пользователя',
        unique=True,
    )
    user_name = models.TextField(
        verbose_name='Username',
        blank=True,
        null=True,
        default='username'
    )
    first_name = models.TextField(
        verbose_name='Имя',
        default='name'
    )

    last_message = models.TextField(
        verbose_name='Последнее сообщение',
        default='',
    )

    def __str__(self):
        return f'{self.external_id} {self.user_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Leaf(models.Model):
    main_menu = models.BooleanField(
        default=False,
        verbose_name='Главное меню',
    )
    leaf = models.CharField(
        verbose_name='Категория',
        max_length=512,
    )

    def __str__(self):
        return f'#{self.id} {self.leaf}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tree(models.Model):
    branch = models.ForeignKey(
        Leaf,
        on_delete=models.CASCADE,
        verbose_name='Ветка',
        related_name='treeBranch'
    )
    leaf = models.ForeignKey(
        Leaf,
        on_delete=models.CASCADE,
        verbose_name='Листок',
        related_name='treeLeaf'
    )

    def __str__(self):
        return f'#{self.branch.leaf}/{self.leaf.leaf}'

    class Meta:
        verbose_name = 'Ветка'
        verbose_name_plural = 'Ветки'


class Bearing(models.Model):
    title = models.CharField(
        verbose_name='Название/Заголовок',
        max_length=128,
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
        default=0,
    )
    photo = models.ImageField(
        upload_to='images',
        verbose_name='Картинка',
        null=True,
    )
    tree = models.ForeignKey(
        Tree,
        verbose_name='Каталог',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.tree}/{self.title}'

    class Meta:
        verbose_name = 'Подшипник'
        verbose_name_plural = 'Подшипники'


class Bearing2(models.Model):
    title = models.CharField(
        verbose_name='Название/Заголовок',
        max_length=128,
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    photo = models.ImageField(
        upload_to='images',
        verbose_name='Картинка',
        null=True,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Подшипник2'
        verbose_name_plural = 'Подшипники2'
