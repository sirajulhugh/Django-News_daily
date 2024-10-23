# Generated by Django 5.1.1 on 2024-09-13 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_newsarticle_published_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoAds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='video_ads/')),
                ('company', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
    ]