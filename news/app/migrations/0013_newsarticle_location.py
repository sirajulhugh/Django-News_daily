# Generated by Django 5.1.1 on 2024-10-02 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsarticle',
            name='location',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
