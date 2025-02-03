import os
import json
import pytest
from app_game_logic.models import Player, Slime, Skill, Item, Inventory, Ennemy
from app_game_logic.game_logic.gameplay.test_algo import *
from app_game_logic.game_logic.gameplay import simple_battle as battle
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
            power=skill_data['power'],
            magic_element=skill_data['magic_element']
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

    ennemies = []
    for ennemy_data in data['ennemy']:
        ennemy = Ennemy.objects.create(
            name=ennemy_data['name'],
            max_hp=ennemy_data['max_hp'],
            hp=ennemy_data['hp'],
            magic_element=ennemy_data['magic_element'],
            attack=ennemy_data['attack'],
            defense=ennemy_data['defense'],
            magic_attack=ennemy_data['magic_attack'],
            magic_defense=ennemy_data['magic_defense'],
            agility=ennemy_data['agility']
        )
        for item_name in ennemy_data['items']:
            ennemy.items.add(items[item_name])
        for skill_name in ennemy_data['skills']:
            ennemy.skills.add(skills[skill_name])
        ennemies.append(ennemy)

    for player_data in data['players']:
        player = players[player_data['username']]
        for item_name in data['items']:
            item = items[item_name['name']]
            Inventory.objects.create(player=player, item=item, quantity=1)

    return players, slimes, items, skills, ennemies

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
        
        # Vérifie les attributs du slime 'Aquatic'
        Aquatic_slime = next(slime for slime in slimes if slime.name == 'Aquatic')
        assert Aquatic_slime.max_hp == 60

        # Vérifie l'association avec les items pour 'Flamy'
        assert items['Sword of Fire'] in flamy_slime.items.all()

        # Vérifie l'association avec les compétences pour 'Flamy'
        assert skills['Fireball'] in flamy_slime.skills.all()
            
@pytest.mark.django_db
class TestBattle:

    def test_make_team(self, setup_test_data):
        players, slimes, items, skills, ennemies = setup_test_data

        for slime in slimes:
            print(f"Slimes : {slime.name} - {slime.skills.all()} -")



        # Front : Input début de combat
        # Création des équipe
        team = GamePlayerTeam(players['Player1'])
        fighter = team.select_fighter()
        gobelin = next(ennemy for ennemy in ennemies if ennemy.name == 'Gobelin')
        ennemy = GameEnnemy(gobelin)
        print(f" Figther : {fighter} VS {ennemy.name}")
        # Envoie des infos au Front (Les slimes en position, les skills du fighter, etc)
        # Attente input Redirection choix
        while fighter.hp > 0 or ennemy.hp > 0:
            first_attacker, second_attacker = battle.is_first_player(fighter, ennemy)

            if first_attacker == fighter:
                input_action = 'attack'  # Placeholder pour l'input du joueur
                enemy_action = ennemy.choose_action()
            else:
                input_action = ennemy.choose_action()  # L'ennemi agit en premier
                enemy_action = 'attack'  # Le joueur attaquera ensuite
            
            # TODO: implémenté le choix user
            print(f" Ennemy hp = {ennemy.hp}")
            damage = battle.handle_action(input_action, first_attacker, second_attacker)

            battle.make_damage(damage, second_attacker)
            if second_attacker.hp <= 0:
                print(f"{second_attacker.name} est KO! {first_attacker.name} remporte la victoire!")
                break
            damage = battle.handle_action(enemy_action, second_attacker, first_attacker)
            battle.make_damage(damage, first_attacker)
            print(f"{first_attacker.name} a {first_attacker.hp} HP restants.")

            # Vérifier si le premier attaquant est KO
            if first_attacker.hp <= 0:
                print(f"{first_attacker.name} est KO! {second_attacker.name} remporte la victoire!")
                break

            fighter = team.select_fighter()
        

        
        
        

        


