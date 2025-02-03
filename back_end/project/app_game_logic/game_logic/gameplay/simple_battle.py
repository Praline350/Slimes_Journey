import random
from app_game_logic.game_logic.models.player import *


def is_first_player(fighterA, fighterB):
    if fighterA.agility >= fighterB.agility:
        return fighterA, fighterB
    else:
        return fighterB, fighterA


# Matrice d'avantages entre éléments
def advantage(element_a, element_b):
    """Retourne l'avantage entre deux éléments selon la matrice."""
    advantage_matrix = {
        "FLAMME": {"FLAMME": 1, "VAGUE": 0.5, "OMBRE": 1, "LUMIERE": 1.5, "METAUX": 2, "ETHERE": 1, "TEMPETE": 1.5, "ECHO": 1, "FUSION": 1, "NEUTRE": 1},
        "VAGUE": {"FLAMME": 2, "VAGUE": 1, "OMBRE": 1, "LUMIERE": 0.5, "METAUX": 0.5, "ETHERE": 1, "TEMPETE": 2, "ECHO": 1, "FUSION": 1, "NEUTRE": 1},
        "OMBRE": {"FLAMME": 1.5, "VAGUE": 1, "OMBRE": 1, "LUMIERE": 2, "METAUX": 1, "ETHERE": 1.5, "TEMPETE": 1, "ECHO": 1, "FUSION": 1, "NEUTRE": 1},
        "LUMIERE": {"FLAMME": 1, "VAGUE": 1.5, "OMBRE": 2, "LUMIERE": 1, "METAUX": 1, "ETHERE": 1, "TEMPETE": 1, "ECHO": 1.5, "FUSION": 1, "NEUTRE": 1},
        "METAUX": {"FLAMME": 0.5, "VAGUE": 2, "OMBRE": 1, "LUMIERE": 1, "METAUX": 1, "ETHERE": 1, "TEMPETE": 2, "ECHO": 1, "FUSION": 1, "NEUTRE": 1},
        "ETHERE": {"FLAMME": 1, "VAGUE": 1, "OMBRE": 1.5, "LUMIERE": 1, "METAUX": 1, "ETHERE": 1, "TEMPETE": 1, "ECHO": 2, "FUSION": 2, "NEUTRE": 1},
        "TEMPETE": {"FLAMME": 1, "VAGUE": 0.5, "OMBRE": 1, "LUMIERE": 1, "METAUX": 1.5, "ETHERE": 1, "TEMPETE": 1, "ECHO": 2, "FUSION": 1, "NEUTRE": 1},
        "ECHO": {"FLAMME": 1, "VAGUE": 1, "OMBRE": 1, "LUMIERE": 1.5, "METAUX": 1, "ETHERE": 2, "TEMPETE": 1, "ECHO": 1, "FUSION": 1.5, "NEUTRE": 1},
        "FUSION": {"FLAMME": 1, "VAGUE": 1, "OMBRE": 1, "LUMIERE": 1, "METAUX": 1, "ETHERE": 1, "TEMPETE": 1, "ECHO": 1, "FUSION": 1, "NEUTRE": 1},
        "NEUTRE": {"FLAMME": 1, "VAGUE": 1, "OMBRE": 1, "LUMIERE": 1, "METAUX": 1, "ETHERE": 1, "TEMPETE": 1, "ECHO": 1, "FUSION": 1, "NEUTRE": 1}
    }

    try:
        return advantage_matrix[element_a][element_b]
    except KeyError:
        raise ValueError(f"Un ou les deux éléments '{element_a}' et '{element_b}' sont invalides.")
    

def is_harmony(fighter, magic_element_attack):
    if fighter.magic_element == magic_element_attack:
        print(f"Harmony !")
        return 1.5
    else:
        print(f"No Harmony !")
        return 1

def handle_action(action, *args, **kwargs):
    # Trier et exécuter l'action selon le choix
    actions = {
        "attack": attack,
        "skill1": use_skill1,
        "skill2": use_skill2,
        "change": change_fighter
    }
    action = action.lower() 
    if action in actions:
        response = actions[action](*args, **kwargs)  # Appelle la méthode correspondant à l'action
        return response
    else:
        print(f"Action '{action}' non reconnue.")
    
    
def attack(fighter, ennemy):
    magic_element = None
    for item in fighter.items:
        if item.type == 'WEAPON':
            attack = item.attack
            magic_element = item.magic_element
    element_avantage = advantage(magic_element, ennemy.magic_element)
    print(f"advanatge : {element_avantage}")
    harmony = is_harmony(fighter, magic_element)
    damage = calculate_damage(fighter, attack, element_avantage, harmony, ennemy)     
    return damage   

def use_skill1(fighter, ennemy):
    
    skill = fighter.skills.first()
    print(f" {fighter.name} utilise {skill.name}")
    attack = skill.power
    magic_element = skill.magic_element
    element_avantage = advantage(magic_element, ennemy.magic_element)
    print(f"Element avantage du skill {element_avantage}")
    harmony = is_harmony(fighter, magic_element)
    damage = calculate_damage(fighter, attack, element_avantage, harmony, ennemy)     
    return damage   

def use_skill2(fighter, ennemy):
    pass


def change_fighter(fighter, new_fighter):
    
    fighter.is_fighter = False
    new_fighter.is_fighter = True
    return 0


def calculate_damage(fighter, skill_power, element_avantage, harmony, ennemy):
    """
    Calcule les dégâts infligés en fonction d'un équilibre dynamique entre attaque et défense.
    À attaque = défense, les dégâts sont réduits de moitié.
    """
    defense = ennemy.defense
    # Ajout de la puissance de la compétence à l'attaque
    total_attack = fighter.attack + skill_power + (fighter.level*2)
    print(f'total att : {total_attack} [ {fighter.attack}+{skill_power}+{fighter.level*2}]')
    
    # Dégâts de base (50 % de l'attaque initiale)
    base_damage = total_attack / 2
    print(f"Dégâts de base (50 % de l'attaque) : {base_damage:.2f}")
    defense *= 2
    # Ajustement basé sur le ratio attaque/défense
    adjustment_factor = max(0.5, total_attack / (defense + 1))  # +1 pour éviter une division par zéro
    print(f"Facteur d'ajustement (attaque/défense) : {adjustment_factor:.2f}  [ {defense} - {adjustment_factor}]")
    
    random_percentage = random.uniform(0.01, 0.05)
    additional_damage = total_attack * random_percentage
    base_damage += additional_damage
    # Dégâts finaux ajustés
    final_damage = base_damage * adjustment_factor * element_avantage * harmony
    print(f"Dégâts ajustés : {final_damage:.2f}")
    # Minimum de 1 dégât
    return max(1, int(final_damage))

def make_damage(damage, ennemy):
    ennemy.hp -= damage
    print(f"{ennemy.name} recois {damage} dégats")


