# Generated by Django 4.2.20 on 2025-06-09 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0001_initial"),
        ("order", "0004_alter_couponmodel_used_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="ordermodel",
            name="payment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="payment.paymentmodel",
            ),
        ),
    ]
