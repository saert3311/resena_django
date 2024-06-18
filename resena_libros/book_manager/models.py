from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (0, 'admin'),
        (1, 'lector'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)

    @property
    def is_admin(self):
        return True if self.user_type == 0 else False

    @property
    def is_reader(self):
        return True if self.user_type == 1 else False


class Genre(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    publication_year = models.PositiveIntegerField()
    cover = models.ImageField(upload_to='covers/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def get_rating_rounded(self):
        reviews = Review.objects.filter(book=self)
        if reviews:
            rating = round(sum([review.rating for review in reviews]) / len(reviews))
        else:
            rating = 0
        return rating

    def get_reviews(self):
        return Review.objects.filter(book=self)

    @property
    def get_reviews_count(self):
        return Review.objects.filter(book=self).count()


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()
    rating = models.PositiveIntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} - {self.user.username}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.name} - {self.created_at}'
