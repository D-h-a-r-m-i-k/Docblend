# Generated by Django 4.2.11 on 2024-04-17 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Doc", "0003_task"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Task",
        ),
    ]
