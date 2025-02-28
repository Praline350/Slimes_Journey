# Generated by Django 5.1.4 on 2025-02-02 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_game_logic', '0024_slime_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ennemy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='ennemy', max_length=100)),
                ('level', models.PositiveIntegerField(default=1)),
                ('max_hp', models.PositiveIntegerField(default=50)),
                ('hp', models.IntegerField(default=50)),
                ('magic_element', models.CharField(choices=[('FLAMME', 'Flamme'), ('VAGUE', 'Vague'), ('OMBRE', 'Ombre'), ('LUMIERE', 'Lumière'), ('METAUX', 'Métaux'), ('ETHERE', 'Éthéré'), ('TEMPESTE', 'Tempête'), ('ECHO', 'Echo'), ('FUSION', 'Fusion')], default='NEUTRE', max_length=10)),
                ('attack', models.IntegerField(default=0)),
                ('defense', models.IntegerField(default=0)),
                ('magic_attack', models.IntegerField(default=0)),
                ('magic_defense', models.IntegerField(default=0)),
                ('agility', models.IntegerField(default=0)),
                ('items', models.ManyToManyField(blank=True, to='app_game_logic.item')),
                ('skills', models.ManyToManyField(blank=True, to='app_game_logic.skill')),
            ],
        ),
    ]
