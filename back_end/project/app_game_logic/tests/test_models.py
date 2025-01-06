import pytest
from app_game_logic.models import Player, Slime, Skill, Weapon, Armor


@pytest.mark.django_db
class TestPlayer:

    def test_create_player_and_slime(self):
        player = Player.objects.create(username='Player')
        assert player.username == 'Player'
        print(f'player : {player.__dict__}')
        slime1 = Slime.objects.create(player=player, name='SlimeTest', magic_element='FEU')
        assert slime1.name == 'SlimeTest'

        print(f'player slime : {[slime.name for slime in player.slimes.all()]}')

        arme1 = Weapon.objects.create(name='Epee des pronfondeur', attack=10, magic_element='EAU')
        armor1 = Armor.objects.create(name="Armure du vide", defense=10)
        assert arme1.name == 'Epee des pronfondeur'
        assert arme1.attack == 10

        slime1.items.add(arme1, armor1)
        for weapon in slime1.weapons:
            print(f"Arme: {weapon.name}, Attaque: {weapon.attack}")
        print(f"Tout : {slime1.get_typed_items()}")
        print(f"All : {slime1.items.all()}")