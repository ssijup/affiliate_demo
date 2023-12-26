# Generated by Django 4.1.4 on 2023-12-24 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0031_alter_refferallink_link_holder_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refferallink',
            name='link_holder_role',
            field=models.CharField(choices=[('admin', 'admin'), ('influencer', 'influencer'), ('organiser', 'organiser')], default='admin', max_length=50),
        ),
    ]