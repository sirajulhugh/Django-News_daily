# Generated by Django 5.1.1 on 2024-10-11 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_profile_saved_articles'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='saved_videos',
            field=models.ManyToManyField(blank=True, to='app.videonews'),
        ),
    ]