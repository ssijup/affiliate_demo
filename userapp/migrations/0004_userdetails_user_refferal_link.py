# Generated by Django 4.2.2 on 2023-12-23 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0003_userdetails_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='user_refferal_link',
            field=models.URLField(default='1'),
        ),
    ]
