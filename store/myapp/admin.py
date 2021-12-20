from django.contrib import admin
from .models import Product,Category,Reccom,Showcase

class ProductAdmin(admin.ModelAdmin):
    list_display = ['code','name','slug','price','available','category','show_image']
    list_filter = ['available']
    search_fields = ['code','name']
    prepopulated_fields = {'slug':['name']}

class ShowcaseAdmin(admin.ModelAdmin):
    list_display = ['name','show_image']

# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Reccom)
admin.site.register(Showcase,ShowcaseAdmin)
