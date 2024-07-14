# Generated by Django 5.0.6 on 2024-07-05 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_emergencycontact_remove_profile_contact_info_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergencycontact',
            name='email',
            field=models.EmailField(default='contact@example.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='example@example.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(default='123-456-7890', max_length=20),
        ),
    ]
