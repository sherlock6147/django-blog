# Generated by Django 3.1.7 on 2021-04-23 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20210423_0358'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.PositiveIntegerField(default=0, verbose_name='Number Of Likes'),
        ),
    ]
