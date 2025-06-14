# Generated by Django 5.2 on 2025-05-06 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="bio",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="name",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
