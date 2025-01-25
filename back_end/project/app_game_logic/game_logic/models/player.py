# Models des class 'Miroir' des joueurs 


class GamePlayerTeam:
    def __init__(self, player_data, equipped_items):
        self.username = player_data.username
        self.slimes = [GameSlime(slime, equipped_items) for slime in player_data.slimes.all() if slime.in_active_team == True]

    def __str__(self):
        return self.username

class GameSlime:
    def __init__(self, slime_data, equipped_items):
        self.name = slime_data.name
        self.max_hp = slime_data.max_hp
        self.hp = slime_data.hp
        self.magic_element = slime_data.magic_element
        self.attack = slime_data.attack
        self.defense = slime_data.defense
        self.magic_attack = slime_data.magic_attack
        self.magic_defense = slime_data.magic_defense
        self.agility = slime_data.agility
        self.weapon = equipped_items
        self.skills = [skill for skill in slime_data.skills.all()]
        

    def __str__(self):
        return self.name
    


