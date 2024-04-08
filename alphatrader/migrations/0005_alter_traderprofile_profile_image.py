# Generated by Django 4.2 on 2024-04-03 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alphatrader", "0004_traderprofile_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="traderprofile",
            name="profile_image",
            field=models.ImageField(
                blank=True,
                default="user_profiles/default_user.jpeg",
                null=True,
                upload_to="user_profiles/",
            ),
        ),
    ]
