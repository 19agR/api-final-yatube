from django.contrib.auth import get_user_model
from django.db import models

GROUP_TITLE_MAX_LENGTH = 200
MODEL_REPR_MAX_LENGTH = 30

User = get_user_model()


class Group(models.Model):
    """Тематическое сообщество публикаций."""

    title = models.CharField(
        'Название',
        max_length=GROUP_TITLE_MAX_LENGTH,
    )
    slug = models.SlugField('Адрес', unique=True)
    description = models.TextField('Описание')

    def __str__(self) -> str:
        return self.title[:MODEL_REPR_MAX_LENGTH]


class Post(models.Model):
    """Публикация пользователя."""

    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='posts/',
        null=True,
        blank=True,
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:MODEL_REPR_MAX_LENGTH]


class Comment(models.Model):
    """Комментарий пользователя к публикации."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация',
    )
    text = models.TextField('Текст')
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def __str__(self) -> str:
        return self.text[:MODEL_REPR_MAX_LENGTH]


class Follow(models.Model):
    """Подписка одного пользователя на публикации другого."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_user_following',
            ),
        )

    def __str__(self) -> str:
        representation = f'{self.user} подписан на {self.following}'
        return representation[:MODEL_REPR_MAX_LENGTH]
