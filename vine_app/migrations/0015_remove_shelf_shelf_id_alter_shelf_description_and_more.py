# Generated by Django 4.1.3 on 2023-02-02 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vine_app', '0014_shelf_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shelf',
            name='shelf_id',
        ),
        migrations.AlterField(
            model_name='shelf',
            name='description',
            field=models.TextField(default='Представляем коллекцию вин, отобранную со вкусом и знанием своего дела'),
        ),
        migrations.AlterField(
            model_name='shelf',
            name='title',
            field=models.CharField(default='Полка', max_length=50),
        ),
    ]