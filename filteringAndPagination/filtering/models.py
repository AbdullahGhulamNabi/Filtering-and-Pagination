from django.db import models
from django.contrib.contenttypes.models import ContentType

# from django.contrib.auth.models import User

class Author(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)  
    name            = models.CharField(max_length=255, blank=True)
    bio             = models.CharField(max_length=255, blank=True)
    date_of_birth   = models.DateField(null=True, blank=True)


class Book(models.Model):
    title           = models.CharField(max_length=255, blank=True, unique=True)
    author          = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author_books")
    Published_date  = models.DateField(null=True, blank=True)


class Genre(models.Model):
    book = models.ManyToManyField(Book, related_name="genre")
    name       = models.CharField(max_length=255, blank=True)


class BlockList(models.Model):
    ip_addr = models.GenericIPAddressField()
