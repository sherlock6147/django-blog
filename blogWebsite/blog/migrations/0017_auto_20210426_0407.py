# Generated by Django 3.1.7 on 2021-04-26 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20210425_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilephoto',
            name='image',
        ),
        migrations.AddField(
            model_name='profilephoto',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='user_images/'),
        ),
    ]
