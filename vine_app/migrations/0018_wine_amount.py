# Generated by Django 4.1.3 on 2023-02-12 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vine_app', '0017_alter_shelf_cabinet'),
    ]

    operations = [
        migrations.AddField(
            model_name='wine',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
