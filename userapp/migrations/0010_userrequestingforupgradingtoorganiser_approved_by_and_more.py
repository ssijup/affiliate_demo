# Generated by Django 4.2.2 on 2023-12-24 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0009_rename_regiondata_regiondatavillage'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrequestingforupgradingtoorganiser',
            name='approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='upgradation_approved_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userrequestingforupgradingtoorganiser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
