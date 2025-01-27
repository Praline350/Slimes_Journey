import os
import json
import pytest
from app_game_logic.models import Player, Slime, Skill, Item, Inventory
from app_game_logic.game_logic.gameplay.test_algo import *
from app_game_logic.game_logic.gameplay.simple_battle import *
from app_game_logic.game_logic.models.player import *



@pytest.fixture
def setup_test_data():
    """Fixture pour charger les données de test à partir d'un fichier JSON"""
    # Charge le fichier JSON
    test_dir = os.path.dirname(os.path.abspath(__file__))  # Répertoire du test
    file_path = os.path.join(test_dir, 'data_test.json')
    with open(file_path, 'r') as f:
        data = json.load(f)

    players = {}
    for player_data in data['players']:
        player = Player.objects.create(username=player_data['username'])
        players[player_data['username']] = player

    skills = {}
    for skill_data in data['skills']:
        skill = Skill.objects.create(
            name=skill_data['name'],
            type=skill_data['type'],
            power=skill_data['power']
        )
        skills[skill_data['name']] = skill

    items = {}
    for item_data in data['items']:
        item = Item.objects.create(
            name=item_data['name'],
            type=item_data['type'],
            description=item_data['description'],
            magic_element=item_data['magic_element'],
            attack=item_data['attack'],
            defense=item_data['defense'],
            magic_attack=item_data['magic_attack'],
            magic_defense=item_data['magic_defense'],
            agility=item_data['agility'],
            price=item_data['price']
        )
        for skill_name in item_data['skills']:
            item.skills.add(skills[skill_name])
        items[item_data['name']] = item

    slimes = []
    for slime_data in data['slimes']:
        player = players[slime_data['player']]
        slime = Slime.objects.create(
            player=player,
            name=slime_data['name'],
            in_active_team=slime_data['in_active_team'],
            is_fighter=slime_data['is_fighter'],
            max_hp=slime_data['max_hp'],
            hp=slime_data['hp'],
            magic_element=slime_data['magic_element'],
            attack=slime_data['attack'],
            defense=slime_data['defense'],
            magic_attack=slime_data['magic_attack'],
            magic_defense=slime_data['magic_defense'],
            agility=slime_data['agility']
        )
        for item_name in slime_data['items']:
            slime.items.add(items[item_name])
        for skill_name in slime_data['skills']:
            slime.skills.add(skills[skill_name])
        slimes.append(slime)

    for player_data in data['players']:
        player = players[player_data['username']]
        for item_name in data['items']:
            item = items[item_name['name']]
            Inventory.objects.create(player=player, item=item, quantity=1)

    return players, slimes, items, skills

@pytest.mark.django_db
class TestPlayer:

    def test_db_data_json(self, setup_test_data):
        players, slimes, items, skills = setup_test_data

        # Vérifie si les slimes 'Flamy' et 'Aquatic' existent dans la liste des slimes
        assert any(slime.name == 'Flamy' for slime in slimes)
        assert any(slime.name == 'Aquatic' for slime in slimes)
        
        # Vérifie les attributs du slime 'Flamy'
        flamy_slime = next(slime for slime in slimes if slime.name == 'Flamy')
        assert flamy_slime.player.username == 'Player1'
        assert flamy_slime.attack == 15
        
        # Vérifie les attributs du slime 'Frosty'
        Aquatic_slime = next(slime for slime in slimes if slime.name == 'Aquatic')
        assert Aquatic_slime.max_hp == 60

        # Vérifie l'association avec les items pour 'Flamy'
        assert items['Sword of Fire'] in flamy_slime.items.all()

        # Vérifie l'association avec les compétences pour 'Flamy'
        assert skills['Fireball'] in flamy_slime.skills.all()

#     def test_slime_dict_data(self):
#         player = Player.objects.create(username='Player')
#         assert player.username == 'Player'
#         slime1 = Slime.objects.create(
#             player=player,
#             name='SlimeTest',
#             magic_element='FEU',
#             attack =10,
#             defense = 10,
#             magic_attack = 15,
#             magic_defense = 12
#             )
#         assert slime1.name == 'SlimeTest'
#         weapon1 = Item.objects.create(name='Epee des pronfondeur', attack=10, magic_element='EAU', price=45)
#         armor1 = Item.objects.create(name="Armure du vide", defense=16)
#         assert weapon1.name == 'Epee des pronfondeur'
#         assert weapon1.attack == 10

#         slime1.items.add(weapon1, armor1)
#         base_att = slime1.attack
#         base_def = slime1.defense
#         base_magic_att = slime1.magic_attack
#         base_magic_def = slime1.magic_defense
            
@pytest.mark.django_db
class TestBattle:

    # def setup_method(self):
    #     self.player = Player.objects.create(username="Player")
    #     self.slime_data1 = {
    #         "name": "Flamy",
    #         "magic_element": "FLAMME",
    #         "in_active_team": True,
    #         "attack": 15,
    #         "defense": 8,
    #         "magic_attack": 18,
    #         "magic_defense": 10,
    #         "agility": 12,
    #     }
    #     self.slime_data2 = {
    #         "name": "Aquarius",
    #         "magic_element": "VAGUE",
    #         "in_active_team": False,
    #         "attack": 10,
    #         "defense": 12,
    #         "magic_attack": 20,
    #         "magic_defense": 15,
    #         "agility": 9,
    #     }
    #     self.slime_data3 = {
    #         "name": "Spectra",
    #         "magic_element": "ETHERE",
    #         "in_active_team": False,
    #         "attack": 8,
    #         "defense": 14,
    #         "magic_attack": 22,
    #         "magic_defense": 18,
    #         "agility": 10,
    #     }
    #     self.slime1 = Slime.objects.create(player=self.player, **self.slime_data1)
    #     self.slime2 = Slime.objects.create(player=self.player, **self.slime_data2)
    #     self.slime3 = Slime.objects.create(player=self.player, **self.slime_data3)
        
    #     self.weapon1 = Item.objects.create(name='Epee des pronfondeur', attack=10, magic_element='VAGUE', price=45, type='ARME')
    #     self.armor1 = Item.objects.create(name="Armure du vide", defense=10, type='ARMURE')
    #     self.slime1.items.add(self.weapon1, self.armor1)
    

    def test_make_team(self, setup_test_data):
        players, slimes, items, skills = setup_test_data

        for slime in slimes:
            print(f"Slimes : {slime.name} - {slime.skills.all()} -")



        # Front : Input début de combat
        # Création des équipe
        teamA = GamePlayerTeam(players['Player1'])
        teamB = GamePlayerTeam(players['Player2'])
        battleA, battleB = init_teams_for_battle(teamA, teamB)
        fighterA = teamA.select_fighter()
        fighterB = teamB.select_fighter()
        print(f" Figther : {fighterA} VS {fighterB}")

        

        # Envvoie des infos au Front (Les slimes en position, les skills du fighter, etc)
        # Attente input Redirecttion choix
        while fighterA.hp > 0 | fighterB.hp > 0:
            first_player, last_player = is_first_player(fighterA, fighterB)
            input = 'attack'
            # TODO: implémenté le choix user
            damageA = battleA.handle_action(input)
            damageB = battleB.handle_action(input)
            if fighterA.agility >= fighterB.agility:
                battleA.make_damage(damageA, fighterB)
                battleB.make_damage(damageB, fighterA)
            else:
                battleB.make_damage(damageB, fighterA)
                battleA.make_damage(damageA, fighterB)
                
            
            fighterA = teamA.select_fighter()
            fighterB = teamB.select_fighter()
        

        
        
        

        


