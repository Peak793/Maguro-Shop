# Generated by Django 3.2.9 on 2021-11-19 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20211119_1954'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommend_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.product')),
            ],
        ),
    ]
