# Generated by Django 5.1.4 on 2025-01-25 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_game_logic', '0011_slime_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='armor',
            name='magic_defense',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='weapon',
            name='magic_attack',
            field=models.IntegerField(default=0),
        ),
    ]
