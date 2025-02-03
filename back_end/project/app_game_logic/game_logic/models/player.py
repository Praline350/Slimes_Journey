# Models des class 'Miroir' des joueurs 
import random

class GamePlayerTeam:
    def __init__(self, player):
        self.username = player.username
        self.slimes = [GameSlime(slime) for slime in player.slimes.all() if slime.in_active_team == True]

    def __str__(self):
        return self.username
    
    def select_fighter(self):
        for slime in self.slimes:
            if slime.is_fighter:
                return slime        
        return None

class GameSlime:
    def __init__(self, slime):
        self.name = slime.name
        self.level = slime.level
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
    
class GameEnnemy:
    def __init__(self, ennemy):
        self.name = ennemy.name
        self.level = ennemy.level
        self.max_hp = ennemy.max_hp
        self.hp = ennemy.hp
        self.magic_element = ennemy.magic_element
        self.attack = ennemy.attack
        self.defense = ennemy.defense
        self.magic_attack = ennemy.magic_attack
        self.magic_defense = ennemy.magic_defense
        self.agility = ennemy.agility
        self.items = ennemy.items.all()
        self.skills = ennemy.skills.all()
        
    def __str__(self):
        return self.name
    
    def choose_action(self):
        actions = ['attack', 'skill1'] # Ajouter les skills à ses choix
        return random.choice(actions)  # Retourne une action aléatoire

    


