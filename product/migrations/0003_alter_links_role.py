# Generated by Django 4.2.2 on 2023-12-22 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='links',
            name='role',
            field=models.CharField(choices=[('influencer', 'influencer'), ('product', 'product'), ('organiser', 'organiser')], default='product', max_length=50),
        ),
    ]