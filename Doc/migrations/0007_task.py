# Generated by Django 4.2.11 on 2024-04-17 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Doc", "0006_delete_task"),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("task", models.CharField(max_length=200)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
