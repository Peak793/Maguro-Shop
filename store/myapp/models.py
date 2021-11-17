from django.db import models

# Create your models here.
class Product(models.Model):
    code = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    price = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)
    available = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to='upload',null=True, blank=True)

    def __str__(self):
        return self.name
