# Generated by Django 3.1.7 on 2021-06-17 16:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('createexp', '0004_post_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(related_name='comments_owned', through='createexp.Comment', to=settings.AUTH_USER_MODEL),
        ),
    ]
