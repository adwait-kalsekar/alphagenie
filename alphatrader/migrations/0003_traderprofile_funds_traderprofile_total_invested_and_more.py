# Generated by Django 4.2 on 2024-04-03 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alphatrader", "0002_alter_traderprofile_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="traderprofile",
            name="funds",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name="traderprofile",
            name="total_invested",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name="traderprofile",
            name="total_returns",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
