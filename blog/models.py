from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.title

class UserEditView(models.Model):
    first_name = models.CharField(max_length=100, default='YourDefaultValueHere')
    last_name = models.CharField(max_length=100, default='YourDefaultValueHere')
    email = models.EmailField()
    username = models.CharField(max_length=50, default='YourDefaultValueHere')
    country = models.CharField(max_length=50, default='YourDefaultValueHere')
 
    
    
    def __str__(self):
        return self.username
    
class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    country = models.CharField(max_length=100)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
