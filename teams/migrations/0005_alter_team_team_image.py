# Generated by Django 5.1.6 on 2025-04-09 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0004_alter_singer_singer_image_alter_team_team_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="team_image",
            field=models.ImageField(
                blank=True, default="unknown.svg", null=True, upload_to=""
            ),
        ),
    ]
