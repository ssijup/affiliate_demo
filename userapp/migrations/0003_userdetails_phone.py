# Generated by Django 4.2.2 on 2023-12-22 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_alter_userdata_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
