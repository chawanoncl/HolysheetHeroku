from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.shortcuts import redirect, reverse



class UserLibrary(models.Model):
    sheets = models.ManyToManyField('Sheet')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username 

    def sheet_list(self):
        return self.sheets.all() 

    class Meta:
        verbose_name = 'User Library'
        verbose_name_plural = 'User Library'

def post_user_signup_receiver(sender, instance, created, *args, **kwargs):
    if created:
        UserLibrary.objects.get_or_create(user=instance)

post_save.connect(post_user_signup_receiver, sender=settings.AUTH_USER_MODEL)

class Author(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.name}"
    
    
    

class Sheet(models.Model):
    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    cover = models.ImageField()
    price = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.title
    
    
    
    def get_absolute_url(self):
        return reverse("sheets:sheet-detail", kwargs={'slug': self.slug})

class Page(models.Model):
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE)
    img = models.ImageField()
    page_number = models.IntegerField()
    def __str__(self):
        return f"{self.sheet.title}-{self.pk}"
