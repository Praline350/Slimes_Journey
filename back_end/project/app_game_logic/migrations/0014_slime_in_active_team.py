# Generated by Django 5.1.4 on 2025-01-25 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_game_logic', '0013_slime_hp_slime_max_hp_alter_slime_magic_element_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='slime',
            name='in_active_team',
            field=models.BooleanField(default=False),
        ),
    ]
