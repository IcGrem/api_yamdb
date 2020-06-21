from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings
from .managers import UserManager


class User(AbstractBaseUser):
    USER_ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(max_length=16, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')
    username = models.SlugField(unique=True, blank=True, null=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Category(models.Model):
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
    year = models.PositiveSmallIntegerField(null=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="categories")#null=True, blank=True, 
    genre = models.ManyToManyField(Genre, related_name="genres")

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="titles")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
    score = models.PositiveSmallIntegerField(null=True)
    pub_date = models.DateTimeField("Дата отзыва", auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comment")
    text = models.TextField()
    pub_date = models.DateTimeField("Дата комментария", auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text

