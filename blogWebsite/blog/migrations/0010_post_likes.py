# Generated by Django 3.1.7 on 2021-04-23 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.PositiveIntegerField(default=0, verbose_name='number of likes'),
        ),
    ]
