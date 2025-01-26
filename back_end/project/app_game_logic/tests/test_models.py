import pytest
from app_game_logic.models import Player, Slime, Skill, Item
from app_game_logic.game_logic.gameplay.test_algo import *
from app_game_logic.game_logic.models.player import *

# def switch_items_class(items):
#     """Items : Queryset of Items"""
#     item_class = []
#     for item in items:
#         weapon = item.weapons  # Cette propriété appelle get_real_instance et retourne l'instance de Weapon si c'est une arme
#         armor = item.armors
#         if weapon:
#             item_class.append(weapon)
#         elif armor:
#             item_class.append(armor)
#     return item_class
#         # if weapon:
#         #     print(f"Weapon attack:{weapon.name} - {weapon.attack}")
#         #     yield weapon
#         # elif armor:
#         #     print(f"armor def: {armor.name} - {armor.defense} ")
#         #     yield armor
#         # else:
#         #     print('No weapon/armor')
#         #     yield None

@pytest.mark.django_db
class TestPlayer:

    def test_create_player_and_slime(self):
        player = Player.objects.create(username='Player')
        assert player.username == 'Player'
        print(f'player : {player.__dict__}')
        slime1 = Slime.objects.create(player=player, name='SlimeTest', magic_element='FEU')
        assert slime1.name == 'SlimeTest'

        print(f'player slime : {[slime.name for slime in player.slimes.all()]}')

        weapon1 = Item.objects.create(name='Epee des pronfondeur', attack=10, magic_element='EAU', price=45)
        armor1 = Item.objects.create(name="Armure du vide", defense=10)
        assert weapon1.name == 'Epee des pronfondeur'
        assert weapon1.attack == 10


    def test_slime_dict_data(self):
        player = Player.objects.create(username='Player')
        assert player.username == 'Player'
        slime1 = Slime.objects.create(
            player=player,
            name='SlimeTest',
            magic_element='FEU',
            attack =10,
            defense = 10,
            magic_attack = 15,
            magic_defense = 12
            )
        assert slime1.name == 'SlimeTest'
        weapon1 = Item.objects.create(name='Epee des pronfondeur', attack=10, magic_element='EAU', price=45)
        armor1 = Item.objects.create(name="Armure du vide", defense=16)
        assert weapon1.name == 'Epee des pronfondeur'
        assert weapon1.attack == 10

        slime1.items.add(weapon1, armor1)
        base_att = slime1.attack
        base_def = slime1.defense
        base_magic_att = slime1.magic_attack
        base_magic_def = slime1.magic_defense
            
@pytest.mark.django_db
class TestBattle:

    def setup_method(self):
        self.player = Player.objects.create(username="Player")
        self.slime_data1 = {
            "name": "Flamy",
            "magic_element": "FLAMME",
            "in_active_team": True,
            "attack": 15,
            "defense": 8,
            "magic_attack": 18,
            "magic_defense": 10,
            "agility": 12,
        }
        self.slime_data2 = {
            "name": "Aquarius",
            "magic_element": "VAGUE",
            "in_active_team": False,
            "attack": 10,
            "defense": 12,
            "magic_attack": 20,
            "magic_defense": 15,
            "agility": 9,
        }
        self.slime_data3 = {
            "name": "Spectra",
            "magic_element": "ETHERE",
            "in_active_team": False,
            "attack": 8,
            "defense": 14,
            "magic_attack": 22,
            "magic_defense": 18,
            "agility": 10,
        }
        self.slime1 = Slime.objects.create(player=self.player, **self.slime_data1)
        self.slime2 = Slime.objects.create(player=self.player, **self.slime_data2)
        self.slime3 = Slime.objects.create(player=self.player, **self.slime_data3)
        
        self.weapon1 = Item.objects.create(name='Epee des pronfondeur', attack=10, magic_element='VAGUE', price=45, type='ARME')
        self.armor1 = Item.objects.create(name="Armure du vide", defense=10, type='ARMURE')
        self.slime1.items.add(self.weapon1, self.armor1)
    

    def test_make_team(self):
        assert self.player.username == 'Player'

        assert self.slime1.name == 'Flamy'
        assert self.slime2.name == 'Aquarius'
        assert self.slime3.name == 'Spectra'
        print(f'slime1 -> {self.slime1.player.username}')
        print(self.player.__dict__)
        print(f" slimes de player {self.player.slimes.all()}")
        for slime in self.player.slimes.all():
            print(slime.items.all())
        team = GamePlayerTeam(self.player)
        for slime in team.slimes:
            for item in slime.items:
                if item.type == 'ARME':

                    print(f"ATT {item.attack}")
                    print(f"magic elmt {item.magic_element}")
            print(f"name {slime.name}")
            print(f" att {slime.attack}")
            print(f' hp {slime.max_hp}')
            print(f" items equipped {slime.items}")

            
        

        


