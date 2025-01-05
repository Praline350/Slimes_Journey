"""
    Modèl player.
    Représente le models de la DB pour les logiques de jeu, et différentes fonctionnalité du joeur
"""


class Player:
    """
    Classe du joueur, le 'slime'.
    args :
        player_id = int -> L'id du joueur
        player_data = dict -> {'att': int, 'def' : int, 'type' : str}
        item_list = list -> ID list of items
    """

    def __init__(self, player_id, player_data, item_list):
        self.id = player_id
        self.attack = player_data["att"]
        self.defense = player_data["def"]
        self.type = player_data["type"]
        self.item_list = item_list

    def calculate_power(self):
        pass


def calculer_avantage(type1, type2):
    """
    Calcule l'avantage de type1 sur type2.

    :param type1: Type de l'attaquant (par exemple, 'feu')
    :param type2: Type de la défense (par exemple, 'plante')
    :return: Le multiplicateur d'avantage (par exemple, 2, 1, ou 0.5)
    """
    advantage_dict = {
        "feu": {"plante": 2, "eau": 0.5, "feu": 1},
        "eau": {"plante": 2, "eau": 1, "feu": 0.5},
        "plante": {"plante": 1, "eau": 0.5, "feu": 2},
    }

    return advantage_dict[type1][type2]
