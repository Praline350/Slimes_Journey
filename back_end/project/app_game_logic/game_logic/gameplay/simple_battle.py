import random
from app_game_logic.game_logic.models.player import *


def init_teams_for_battle(teamA, teamB):
    battle_control_1 = BatlleControl(teamA, teamB)
    battle_control_2 = BatlleControl(teamA, teamB)
    return battle_control_1, battle_control_2

def is_first_player(fighterA, fighterB):
    if fighterA.agility >= fighterB.agility:
        return fighterA, fighterB
    else:
        return fighterB, fighterA
    
# Matrice d'avantages entre éléments


def advantage(element_a, element_b):
    """Retourne l'avantage entre deux éléments selon la matrice."""
    advantage_matrix = {
    "FLAMME": {
        "FLAMME": 1, "VAGUE": 0.5, "OMBRE": 1, "LUMIERE": 1.5, "METAUX": 2, "ETHERE": 1, "TEMPETE": 1.5, "ECHO": 1, "FUSION": 1
    },
    "VAGUE": {
        "FLAMME": 2, "VAGUE": 1, "OMBRE": 1, "LUMIERE": 0.5, "METAUX": 0.5, "ETHERE": 1, "TEMPETE": 2, "ECHO": 1, "FUSION": 1
    },
    "OMBRE": {
        "FLAMME": 1.5, "VAGUE": 1, "OMBRE": 1, "LUMIERE": 2, "METAUX": 1, "ETHERE": 1.5, "TEMPETE": 1, "ECHO": 1, "FUSION": 1
    },
    "LUMIERE": {
        "FLAMME": 1, "VAGUE": 1.5, "OMBRE": 2, "LUMIERE": 1, "METAUX": 1, "ETHERE": 1, "TEMPETE": 1, "ECHO": 1.5, "FUSION": 1
    },
    "METAUX": {
        "FLAMME": 0.5, "VAGUE": 2, "OMBRE": 1, "LUMIERE": 1, "METAUX": 1, "ETHERE": 1, "TEMPETE": 2, "ECHO": 1, "FUSION": 1
    },
    "ETHERE": {
        "FLAMME": 1, "VAGUE": 1, "OMBRE": 1.5, "LUMIERE": 1, "METAUX": 1, "ETHERE": 1, "TEMPETE": 1, "ECHO": 2, "FUSION": 2
    },
    "TEMPETE": {
        "FLAMME": 1, "VAGUE": 0.5, "OMBRE": 1, "LUMIERE": 1, "METAUX": 1.5, "ETHERE": 1, "TEMPETE": 1, "ECHO": 2, "FUSION": 1
    },
    "ECHO": {
        "FLAMME": 1, "VAGUE": 1, "OMBRE": 1, "LUMIERE": 1.5, "METAUX": 1, "ETHERE": 2, "TEMPETE": 1, "ECHO": 1, "FUSION": 1.5
    },
    "FUSION": {
        "FLAMME": 1, "VAGUE": 1, "OMBRE": 1, "LUMIERE": 1, "METAUX": 1, "ETHERE": 1, "TEMPETE": 1, "ECHO": 1, "FUSION": 1
    }
}

    try:
        return advantage_matrix[element_a][element_b]
    except KeyError:
        raise ValueError(f"Un ou les deux éléments '{element_a}' et '{element_b}' sont invalides.")
    

def is_harmony(fighter, magic_element_attack):
    if fighter.magic_element == magic_element_attack:
        return 1.5
    else:
        return 1

class BatlleControl:
    def __init__(self, teamA, teamB):
        self.teamA = teamA
        self.ennemy = teamB
        self.actions = {
            "attack": self.attack,
            "skill1": self.use_skill1,
            "skill2": self.use_skill2,
            "change": self.change_fighter
        }

    def handle_action(self, action):
        # Trier et exécuter l'action selon le choix
        action = action.lower() 
        if action in self.actions:
            response = self.actions[action]()  # Appelle la méthode correspondant à l'action
        else:
            print(f"Action '{action}' non reconnue.")
        return response
        
    def attack(self):
        print(f"{self.teamA.username} attaque !")
        fighter = self.teamA.select_fighter()
        ennemy = self.ennemy.select_fighter()
        magic_element = None
        for item in fighter.items:
            if item.type == 'WEAPON':
                attack = item.attack
                magic_element = item.magic_element
        element_avantage = advantage(magic_element, ennemy.magic_element)
        harmony = is_harmony(fighter, magic_element)
        damage = self.calculate_damage(fighter, attack, element_avantage, harmony)     
        return damage   

    def use_skill1(self):
        print(f"{self.teamA.username} utilise Skill 1!")
        # Implémenter la logique de l'utilisation de skill1 ici

    def use_skill2(self):
        print(f"{self.teamA.username} utilise Skill 2!")
        # Implémenter la logique de l'utilisation de skill2 ici

    def change_fighter(self):
        print(f"{self.teamA.username} change de slime!")
        # Implémenter la logique de changement de fighter ici


    def calculate_damage(self, slime, skill_power, element_avantage, harmony):
        """
        Calcule les dégâts infligés en fonction d'un équilibre dynamique entre attaque et défense.
        À attaque = défense, les dégâts sont réduits de moitié.
        """
        ennemy = self.ennemy.select_fighter()
        defense = ennemy.defense
        # Ajout de la puissance de la compétence à l'attaque
        total_attack = slime.attack + skill_power + (slime.level*2)
        print(f'total att : {total_attack} [ {slime.attack}+{skill_power}+{slime.level*2}]')
        
        # Dégâts de base (50 % de l'attaque initiale)
        base_damage = total_attack / 2
        print(f"Dégâts de base (50 % de l'attaque) : {base_damage:.2f}")
        defense *= 2
        # Ajustement basé sur le ratio attaque/défense
        adjustment_factor = total_attack / ((defense) + 1)  # +1 pour éviter une division par zéro
        print(f"Facteur d'ajustement (attaque/défense) : {adjustment_factor:.2f}  [ {defense} - {adjustment_factor}]")
        
        random_percentage = random.uniform(0.01, 0.05)
        additional_damage = total_attack * random_percentage
        base_damage += additional_damage
        # Dégâts finaux ajustés
        final_damage = base_damage * adjustment_factor * element_avantage * harmony
        print(f"Dégâts ajustés : {final_damage:.2f}")
        # Minimum de 1 dégât
        return max(1, int(final_damage))
    
    def make_damage(self, damage, ennemy):
        ennemy.hp -= damage
        print(f"{ennemy.name} recois {damage} dégats")


