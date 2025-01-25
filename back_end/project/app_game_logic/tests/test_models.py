import pytest
from app_game_logic.models import Player, Slime, SlimeItem, Skill, Weapon, Armor
from app_game_logic.game_logic.gameplay.test_algo import *
from app_game_logic.game_logic.models.player import *

def switch_items_class(items):
    """Items : Queryset of Items"""
    item_class = []
    for item in items:
        weapon = item.weapons  # Cette propriété appelle get_real_instance et retourne l'instance de Weapon si c'est une arme
        armor = item.armors
        if weapon:
            item_class.append(weapon)
        elif armor:
            item_class.append(armor)
    return item_class
        # if weapon:
        #     print(f"Weapon attack:{weapon.name} - {weapon.attack}")
        #     yield weapon
        # elif armor:
        #     print(f"armor def: {armor.name} - {armor.defense} ")
        #     yield armor
        # else:
        #     print('No weapon/armor')
        #     yield None

@pytest.mark.django_db
class TestPlayer:

    def test_create_player_and_slime(self):
        player = Player.objects.create(username='Player')
        assert player.username == 'Player'
        print(f'player : {player.__dict__}')
        slime1 = Slime.objects.create(player=player, name='SlimeTest', magic_element='FEU')
        assert slime1.name == 'SlimeTest'

        print(f'player slime : {[slime.name for slime in player.slimes.all()]}')

        weapon1 = Weapon.objects.create(name='Epee des pronfondeur', attack=10, magic_element='EAU', price=45)
        armor1 = Armor.objects.create(name="Armure du vide", defense=10)
        assert weapon1.name == 'Epee des pronfondeur'
        assert weapon1.attack == 10

        SlimeItem.objects.create(slime=slime1, item=weapon1, quantity=4)
        SlimeItem.objects.create(slime=slime1, item=armor1, quantity=2)
        all_items = SlimeItem.objects.filter(slime=slime1)
        print(f'slime item : {all_items}')

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
        weapon1 = Weapon.objects.create(name='Epee des pronfondeur', attack=10, magic_element='EAU', price=45)
        armor1 = Armor.objects.create(name="Armure du vide", defense=16)
        assert weapon1.name == 'Epee des pronfondeur'
        assert weapon1.attack == 10

        slime1.items.add(weapon1, armor1)
        weapon = SlimeItem.objects.filter(slime=slime1, item=weapon1).first()
        armor = SlimeItem.objects.filter(slime=slime1, item=armor1).first()
        weapon.is_equipped = True
        armor.is_equipped = True
        weapon.save()
        armor.save()
        base_att = slime1.attack
        base_def = slime1.defense
        base_magic_att = slime1.magic_attack
        base_magic_def = slime1.magic_defense
        equipped_items = SlimeItem.get_equipped_items(slime1)
        print(f'equipepment equipé : {equipped_items}')
        list = switch_items_class(equipped_items)
        print(f'list {list}')
        for item in list:
            if isinstance(item, Weapon):
                power_att = item.attack

            elif isinstance(item, Armor):
                base_def += item.defense
        print(f'damage :{calculate_damage_poké(45, power_att, base_att, base_def)}')

        print(f" my algo damage : {calculate_damage(7, base_att, power_att, 10)}")



            
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
        
        self.weapon1 = Weapon.objects.create(name='Epee des pronfondeur', attack=10, magic_element='VAGUE', price=45)
        self.armor1 = Armor.objects.create(name="Armure du vide", defense=10)
        self.slime1.items.add(self.weapon1, self.armor1)
        weapon = SlimeItem.objects.filter(slime=self.slime1, item=self.weapon1).first()
        armor = SlimeItem.objects.filter(slime=self.slime1, item=self.armor1).first()
        weapon.is_equipped = True
        armor.is_equipped = True
        weapon.save()
        armor.save()

    def test_make_team(self):
        assert self.player.username == 'Player'

        assert self.slime1.name == 'Flamy'
        assert self.slime2.name == 'Aquarius'
        assert self.slime3.name == 'Spectra'
        print(f'slime1 -> {self.slime1.player.username}')
        print(self.player.__dict__)
        print(f" slimes de player {self.player.slimes.all()}")
        for slime in self.player.slimes.all():
            if slime.in_active_team == True:
                equipped_items = SlimeItem.get_equipped_items(slime)
                print(equipped_items)
        team = GamePlayerTeam(self.player)
        
            # equipped_items = SlimeItem.get_equipped_items(slime)
            # print(equipped_items)

            # print(slime.name)
            # print(slime.attack)
            # print(slime.max_hp)

            
        

        


