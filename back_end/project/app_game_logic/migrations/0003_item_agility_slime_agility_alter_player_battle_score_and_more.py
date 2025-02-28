# Generated by Django 5.1.4 on 2025-01-02 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_game_logic', '0002_alter_slime_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='agility',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='slime',
            name='agility',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='battle_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='coins',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
