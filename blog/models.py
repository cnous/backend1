from django.db import models
from accounts.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    #this is a class for defining posts for blog  app
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    status = models.BooleanField()
    # inja esm ra string dar nazar migirim ta tartib mohem nabashad
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    created_date = models.DateField(auto_now_add=True)
    created_update = models.DateField(auto_now_add=True)
    published_date = models.DateField()

    def __str__(self):
        return self.title
    def get_snippet(self):
        return self.content[0:5]


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

