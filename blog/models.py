from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Category(MPTTModel):
    """Класс модели категорий"""
    name = models.CharField(max_length=150, verbose_name='наименование', **NULLABLE)
    slug = models.SlugField(max_length=100, **NULLABLE)
    parent = TreeForeignKey(
        'self',
        related_name="children_of_mptt",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['name']


class Post(models.Model):
    """Класс модели постов"""
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE, default=True)
    title = models.CharField(max_length=200, **NULLABLE)
    image = models.ImageField(upload_to='images/', **NULLABLE)
    text = models.TextField(**NULLABLE)
    category = models.ForeignKey(
        Category,
        related_name="post",
        on_delete=models.SET_NULL,
        null=True
    )

    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', **NULLABLE)
    slug = models.SlugField(max_length=200, unique=True, **NULLABLE)
    published = models.BooleanField(verbose_name='признак публикации', default=True, **NULLABLE)
    view_count = models.PositiveIntegerField(verbose_name='количество просмотров', default=0)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def get_comments(self):
        return self.comment.all()

    def increase_views(self):
        """
        Увеличивает просмотры поста на 1.
        """
        self.view_count += 1
        self.save()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('create_at',)


class Comment(models.Model):
    """Класс модели комментариев"""
    name = models.CharField(max_length=50, **NULLABLE)
    email = models.CharField(max_length=100, **NULLABLE)
    website = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField(max_length=500, **NULLABLE)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', **NULLABLE)
    post = models.ForeignKey(Post, related_name="comment", on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
