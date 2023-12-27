# Generated by Django 4.2.2 on 2023-12-26 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0044_rename_user_details_payment_paying_user_details_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='refferal_link',
            new_name='user_link',
        ),
        migrations.RenameField(
            model_name='paymentrquest',
            old_name='order_id',
            new_name='pay_request_order_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='paying_user_details',
        ),
        migrations.AddField(
            model_name='payment',
            name='pay_request_order_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_done_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_order_id',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_signature',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_status_of_gateway',
            field=models.CharField(default='failed', max_length=25),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_total_amount_paid',
            field=models.IntegerField(default=0),
        ),
    ]