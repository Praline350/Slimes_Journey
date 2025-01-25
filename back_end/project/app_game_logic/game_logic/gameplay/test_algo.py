import random

def calculate_damage(
    level: int,
    attacker_atk: int,
    skill_power: int,
    defender_def: int,
    harmony : float = 1.0,
    element_avantage: float = 1,
    
    
) -> int:
    """
    Calcule les dégâts infligés en fonction d'un équilibre dynamique entre attaque et défense.
    À attaque = défense, les dégâts sont réduits de moitié.
    """

    # Ajout de la puissance de la compétence à l'attaque
    total_attack = attacker_atk + skill_power + (level*2)
    print(f'total att : {total_attack} [ {attacker_atk}+{skill_power}+{level*2}]')
    
    # Dégâts de base (50 % de l'attaque initiale)
    base_damage = total_attack / 2
    print(f"Dégâts de base (50 % de l'attaque) : {base_damage:.2f}")
    defender_def *= 2
    # Ajustement basé sur le ratio attaque/défense
    adjustment_factor = total_attack / ((defender_def) + 1)  # +1 pour éviter une division par zéro
    print(f"Facteur d'ajustement (attaque/défense) : {adjustment_factor:.2f}  [ {defender_def} - {adjustment_factor}]")
    
    random_percentage = random.uniform(0.01, 0.05)
    additional_damage = total_attack * random_percentage
    base_damage += additional_damage
    # Dégâts finaux ajustés
    final_damage = base_damage * adjustment_factor * element_avantage * harmony
    print(f"Dégâts ajustés : {final_damage:.2f}")
    # Minimum de 1 dégât
    return max(1, int(final_damage))

def calculate_damage_poké(
    level : int,
    power_att : int,
    attack : int,
    defense : int,
    harmony : float = 1.0,
    element_avantage : float = 1.0,
) -> int:

    base_dommage = (((2*level)/5+2)*power_att*(attack/defense)/5)
    print(f"base damages : {base_dommage}")
    random_factor = random.uniform(0.85, 1.0)
    base_dommage *= random_factor
    print(power_att, attack, defense)
    return max(1, int(base_dommage * harmony * element_avantage))

if __name__ == "__main__":


    print(calculate_damage_poké(20, 60, 55, 30, 1.5, 1))
     
