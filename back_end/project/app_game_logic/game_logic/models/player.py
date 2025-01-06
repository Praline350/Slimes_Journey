# Models des class 'Miroir' des joueurs 


class GamePlayer:
    def __init__(self, player_data):
        self.username = player_data['username']
        self.slimes = [GameSlime(slime) for slime in player_data.slimes.all()]
        
    def init_team(self, slimes):
        team = GameTeam(self.player, slimes)
        return team

    def __str__(self):
        return self.username

class GameSlime:
    def __init__(self, slime_data):
        self.name = slime_data['name']
        self.magic_element = slime_data['magic_element']
        self.attack = slime_data['attack']
        self.defense = slime_data['defense']
        self.agility = slime_data['agility']
        self.items = [item for item in slime_data.items_set.all()]
        self.skills = [skill for skill in slime_data.skills_set.all()]
        

    def __str__(self):
        return self.name
    

class GameTeam:
    def __init__(self, player, slimes=list):
        self.player = player
        self.slime1 = slimes[0]
        self.slime2 = slimes[1]
        self.slime3 = slimes[1]

    def __str__(self):
        return f"{self.player.username}'s Team"
    
def make_player_team(player_data):
    player = GamePlayer(player_data)
    team = player.init_team(player.slimes)
    return team

