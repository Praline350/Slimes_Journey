# Models des class 'Miroir' des joueurs 


class GamePlayerTeam:
    def __init__(self, player):
        self.username = player.username
        self.slimes = [GameSlime(slime) for slime in player.slimes.all() if slime.in_active_team == True]

    def __str__(self):
        return self.username
    
    def select_figther(self):
        for slime in self.slimes:
            if slime.is_figter:
                return slime
            else:
                return None

class GameSlime:
    def __init__(self, slime):
        self.name = slime.name
        self.is_fighter = slime.is_fighter
        self.max_hp = slime.max_hp
        self.hp = slime.hp
        self.magic_element = slime.magic_element
        self.attack = slime.attack
        self.defense = slime.defense
        self.magic_attack = slime.magic_attack
        self.magic_defense = slime.magic_defense
        self.agility = slime.agility
        self.items = slime.items.all()
        self.skills = slime.skills.all()
        

    def __str__(self):
        return self.name
    


