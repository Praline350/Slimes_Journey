import random

class BatlleControl:
    def __init__(self, player, ennemy):
        self.player = player
        self.ennemy = ennemy
    
    def process_choice(self, input):
        """Definis si l'action est une attaque(cac ou magic) ou un changment de statut"""
        pass

    def calculate_damage(self, slime, skill_power, element_avantage, harmony):
        """
        Calcule les dégâts infligés en fonction d'un équilibre dynamique entre attaque et défense.
        À attaque = défense, les dégâts sont réduits de moitié.
        """

        # Ajout de la puissance de la compétence à l'attaque
        total_attack = slime.attack + skill_power + (slime.level*2)
        print(f'total att : {total_attack} [ {slime.attack}+{skill_power}+{slime.level*2}]')
        
        # Dégâts de base (50 % de l'attaque initiale)
        base_damage = total_attack / 2
        print(f"Dégâts de base (50 % de l'attaque) : {base_damage:.2f}")
        self.ennemy.defense *= 2
        # Ajustement basé sur le ratio attaque/défense
        adjustment_factor = total_attack / ((self.ennemy.defense) + 1)  # +1 pour éviter une division par zéro
        print(f"Facteur d'ajustement (attaque/défense) : {adjustment_factor:.2f}  [ {self.ennemy.defense} - {adjustment_factor}]")
        
        random_percentage = random.uniform(0.01, 0.05)
        additional_damage = total_attack * random_percentage
        base_damage += additional_damage
        # Dégâts finaux ajustés
        final_damage = base_damage * adjustment_factor * element_avantage * harmony
        print(f"Dégâts ajustés : {final_damage:.2f}")
        # Minimum de 1 dégât
        return max(1, int(final_damage))
