# Generated by Django 3.2.9 on 2021-11-19 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20211119_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommend_list',
            name='products',
            field=models.ManyToManyField(blank=True, to='myapp.Product'),
        ),
    ]
