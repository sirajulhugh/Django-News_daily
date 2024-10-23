# Generated by Django 5.1.1 on 2024-10-07 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_imageads_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageads',
            name='image',
            field=models.ImageField(upload_to='media/ads_images/'),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='image',
            field=models.ImageField(upload_to='media/article_images/'),
        ),
        migrations.AlterField(
            model_name='storycard',
            name='image',
            field=models.ImageField(upload_to='media/story_images/'),
        ),
        migrations.AlterField(
            model_name='videoads',
            name='video',
            field=models.FileField(upload_to='media/video_ads/'),
        ),
        migrations.AlterField(
            model_name='videonews',
            name='video',
            field=models.FileField(upload_to='media/videos/'),
        ),
    ]
