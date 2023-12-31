# Generated by Django 4.2.2 on 2023-12-25 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0012_remove_userdetails_user_refferal_link'),
        ('product', '0035_product_full_fillment_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='refferallink',
            name='user_details',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_details_parameters', to='userapp.userdetails'),
        ),
        migrations.AddField(
            model_name='refferallink',
            name='user_refferal_link',
            field=models.URLField(default='1'),
        ),
        migrations.AlterField(
            model_name='refferallink',
            name='link_holder_role',
            field=models.CharField(choices=[('organiser', 'organiser'), ('influencer', 'influencer'), ('admin', 'admin')], default='admin', max_length=50),
        ),
    ]
