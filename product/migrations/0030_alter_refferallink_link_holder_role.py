# Generated by Django 4.2.2 on 2023-12-24 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_remove_payment_user_payment_refferal_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refferallink',
            name='link_holder_role',
            field=models.CharField(choices=[('admin', 'admin'), ('influencer', 'influencer'), ('organiser', 'organiser')], default='admin', max_length=50),
        ),
    ]