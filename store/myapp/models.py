from django.db import models
from django.utils.html import format_html
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = 'Catagories'

    def __str__(self):
        return self.name

class Showcase(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to='upload',null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    code = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    slug = models.SlugField(max_length=200, unique=True,null=True)
    price = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)
    available = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to='upload',null=True, blank=True)
    showcase = models.ManyToManyField(Showcase)
    category = models.ForeignKey(Category, null=True,blank=True,on_delete= models.CASCADE)

    def __str__(self):
        return self.name
    
    def show_image(self):
        if self.image:
            return format_html('<img src="%s" height="50px">' % self.image.url)
        return ''

class Reccom(models.Model):
    code = models.CharField(max_length=10 ,null=True,blank=True)
    product = models.ForeignKey(Product, null=True,blank=True,on_delete= models.CASCADE)

    def __str__(self):
        return self.code