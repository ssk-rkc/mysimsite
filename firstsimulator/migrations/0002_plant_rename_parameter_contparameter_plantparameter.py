# Generated by Django 4.2.11 on 2024-05-02 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("firstsimulator", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Plant",
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
                ("plant_type", models.CharField(max_length=200)),
                (
                    "plant_name",
                    models.CharField(max_length=200, verbose_name="plant name"),
                ),
            ],
        ),
        migrations.RenameModel(
            old_name="Parameter",
            new_name="contParameter",
        ),
        migrations.CreateModel(
            name="plantParameter",
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
                ("processGain", models.IntegerField(default=555555)),
                ("timeConst1", models.IntegerField(default=5555555)),
                ("timeConst2", models.IntegerField(default=5555555)),
                ("timeConst3", models.IntegerField(default=5555555)),
                (
                    "plant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="firstsimulator.plant",
                    ),
                ),
            ],
        ),
    ]