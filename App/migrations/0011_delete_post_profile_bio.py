# Generated by Django 5.0.6 on 2024-07-13 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_alter_comment_post'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='Bio information not provided'),
        ),
    ]
