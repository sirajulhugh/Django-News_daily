# Generated by Django 5.1.1 on 2024-09-11 11:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VisualStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visual_stories', to='app.category')),
            ],
        ),
        migrations.CreateModel(
            name='StoryCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='story_images/')),
                ('heading', models.CharField(max_length=255)),
                ('short_text', models.TextField(max_length=500)),
                ('visual_story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='story_cards', to='app.visualstory')),
            ],
        ),
    ]
