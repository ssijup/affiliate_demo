# Generated by Django 4.2.2 on 2023-12-25 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0039_alter_refferallink_link_holder_role_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refferallink',
            name='link_holder_role',
        ),
        migrations.AddField(
            model_name='refferallink',
            name='link_holder_current_role',
            field=models.CharField(choices=[('organiser', 'organiser'), ('influencer', 'influencer'), ('admin', 'admin')], default='admin', max_length=50),
        ),
        migrations.AddField(
            model_name='refferallink',
            name='link_holder_role_at_link_generation',
            field=models.CharField(choices=[('organiser', 'organiser'), ('influencer', 'influencer'), ('admin', 'admin')], default='admin', max_length=50),
        ),
    ]
