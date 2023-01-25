# Generated by Django 4.1.3 on 2022-11-14 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vine_app', '0008_wine_winery'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shelf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shelf_id', models.IntegerField(unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='wine',
            name='wine_image',
            field=models.ImageField(default='default.jpg', upload_to='img/'),
        ),
    ]