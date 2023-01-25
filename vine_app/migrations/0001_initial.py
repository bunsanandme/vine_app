# Generated by Django 4.1.3 on 2022-11-13 10:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wine',
            fields=[
                ('wine_id', models.AutoField(primary_key=True, serialize=False)),
                ('wine_name', models.CharField(max_length=50)),
                ('crop_year', models.PositiveIntegerField(help_text='Use the following format: <YYYY>', validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2022)])),
                ('region', models.CharField(max_length=60)),
                ('fragrance', models.CharField(max_length=100)),
                ('taste', models.CharField(max_length=100)),
                ('fun_facts', models.TextField()),
            ],
        ),
    ]