from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    full_name = models.TextField()
    birth_year = models.SmallIntegerField()
    country = models.CharField(max_length=2)

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})

class Publisher(models.Model):
    name = models.TextField(max_length=128)

    def __str__(self):
        return self.name

class Friend(models.Model):
    name = models.TextField(max_length=128)

    def __str__(self):
        return self.name

class Book(models.Model):
    ISBN = models.CharField(max_length=13)
    title = models.TextField()
    description = models.TextField()  
    year_release = models.SmallIntegerField()  
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    copy_count = models.SmallIntegerField(default=1)
    image = models.ImageField(upload_to='media/picture', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True)
    reader = models.ForeignKey(Friend, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
