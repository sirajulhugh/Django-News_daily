# Generated by Django 5.1.1 on 2024-10-05 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_videonews_location_visualstory_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageads',
            name='link',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]