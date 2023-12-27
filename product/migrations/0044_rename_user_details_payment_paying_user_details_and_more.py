# Generated by Django 4.2.2 on 2023-12-26 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0043_alter_refferallink_link_holder_current_role_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='user_details',
            new_name='paying_user_details',
        ),
        migrations.AddField(
            model_name='payment',
            name='Product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.AddField(
            model_name='paymentrquest',
            name='order_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='paymentrquest',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.AddField(
            model_name='paymentrquest',
            name='user_link',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.refferallink'),
        ),
        migrations.AlterField(
            model_name='refferallink',
            name='link_holder_current_role',
            field=models.CharField(choices=[('influencer', 'influencer'), ('admin', 'admin'), ('organiser', 'organiser')], default='admin', max_length=50),
        ),
        migrations.AlterField(
            model_name='refferallink',
            name='link_holder_role_at_link_generation',
            field=models.CharField(choices=[('influencer', 'influencer'), ('admin', 'admin'), ('organiser', 'organiser')], default='admin', max_length=50),
        ),
    ]
