# Generated by Django 5.1.1 on 2024-09-20 13:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_newsarticle'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('category1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category1', to='app.category')),
                ('category2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category2', to='app.category')),
                ('category3', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category3', to='app.category')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
