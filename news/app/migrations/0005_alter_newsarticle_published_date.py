# Generated by Django 5.1.1 on 2024-09-12 05:32

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_newsarticle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsarticle',
            name='published_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
