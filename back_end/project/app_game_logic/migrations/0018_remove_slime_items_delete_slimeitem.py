# Generated by Django 5.1.4 on 2025-01-25 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_game_logic', '0017_item_attack_item_defense_item_magic_attack_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slime',
            name='items',
        ),
        migrations.DeleteModel(
            name='SlimeItem',
        ),
    ]
