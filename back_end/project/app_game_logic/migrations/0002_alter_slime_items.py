# Generated by Django 5.1.4 on 2025-01-02 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_game_logic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slime',
            name='items',
            field=models.ManyToManyField(blank=True, to='app_game_logic.item'),
        ),
    ]
