# Generated by Django 5.1.6 on 2025-03-11 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0005_team_user_id_alter_singer_name_alter_team_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="teammember",
            name="added_by",
        ),
    ]
