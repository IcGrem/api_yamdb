from django.contrib.auth import get_user_model
from django.db import models
import datetime


User = get_user_model()

class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)


    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateTimeField(default = datetime.datetime.now().year)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, related_name="title_category")
    genre = models.ManyToManyField(Genre, verbose_name='genres')
    #genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name="title_genre")

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="title")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
    score = models.PositiveSmallIntegerField(default=1, null=True)
    pub_date = models.DateTimeField("Дата review", auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comment")
    text = models.TextField()
    created = models.DateTimeField("Дата комментария", auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text