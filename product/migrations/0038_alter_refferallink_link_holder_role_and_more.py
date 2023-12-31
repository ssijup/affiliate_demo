# Generated by Django 4.2.2 on 2023-12-25 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0037_alter_refferallink_link_holder_role_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refferallink',
            name='link_holder_role',
            field=models.CharField(choices=[('influencer', 'influencer'), ('admin', 'admin'), ('organiser', 'organiser')], default='admin', max_length=50),
        ),
        migrations.AlterField(
            model_name='refferallink',
            name='user_refferal_link',
            field=models.URLField(default='1'),
        ),
    ]
