from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Title(models.Model):
    name = models.CharField(max_length=200, verbose_name="Наименование")
    year = models.IntegerField(db_index=True, verbose_name="Год")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="titles"
    )
    description = models.TextField(verbose_name="Описание")
    category = models.ForeignKey(
        "Categories",
        null=True,
        on_delete=models.SET_NULL,
        related_name="title",
        verbose_name="Категория"
    )
    genre = models.ManyToManyField(
        "Genres",
        related_name="title",
        verbose_name="Жанр"
    )

    class Meta():
        ordering = ["year"]

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        "Дата и время публикации",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        unique_together = ('title', 'author')

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Дата и время публикации",
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.author}, {self.pub_date}: {self.text[:15]}'
