# Generated by Django 4.1.3 on 2022-11-13 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vine_app', '0004_alter_wine_wine_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wine',
            name='wine_image',
            field=models.ImageField(default='default.jpg', upload_to='\\media\\'),
        ),
    ]
