from django.db import models
from django.contrib.auth.models import User
from .constants import ACCOUNT_TYPE,TRANSACTION_TYPE
from accounts.models import UserAccount

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True,null=True,blank=True)


    def __str__(self):
        return self.name 


class Books(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    Title=models.TextField()
    price=models.IntegerField()
    category=models.OneToOneField(Category,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='Books/media/uploads/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True) 

    def __str__(self):
        return self.name

class Comment(models.Model):
    post=models.ForeignKey(Books,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=30)
    body=models.TextField()
    
    def __str__(self):
        return f"Comments by{self.name}"





STATUS_CHOICES = [
    ('borrowed', 'borrowed'),
    ('returned', 'returned'),
]






class Borrow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="book")
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="borrowed")

    def __str__(self) -> str:
        return f"{self.user.username}"

    def __str__(self) -> str:
        return f"{self.user.username}"
    


