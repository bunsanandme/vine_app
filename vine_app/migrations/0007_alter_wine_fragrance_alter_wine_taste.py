# Generated by Django 4.1.3 on 2022-11-13 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vine_app', '0006_alter_wine_wine_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wine',
            name='fragrance',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='wine',
            name='taste',
            field=models.CharField(max_length=200),
        ),
    ]
