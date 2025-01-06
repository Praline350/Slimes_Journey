from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

ELEMENTS_CHOICE = [("EAU", "Eau"), ("FEU", "Feu"), ("AIR", "Air"), ("TERRE", "Terre"), ('NEUTRE', 'Neutre')]
ITEMS_TYPE_CHOICE = [("ARME", "Arme"), ("ARMURE", "Armure")]
SKILL_TYPE_CHOICE = [("ACTIVE", "Active"), ("PASSIVE", "Passive")]


class Skill(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    type = models.CharField(max_length=15, choices=SKILL_TYPE_CHOICE)

class Item(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(null=True, blank=True)
    agility = models.IntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.name
    
    def get_real_instance(self):
        """
        Retourne l'instance de la sous-classe si elle existe
        """
        if hasattr(self, 'weapon'):
            return self.weapon
        elif hasattr(self, 'armor'):
            return self.armor
        return self

class Weapon(Item):
    attack = models.IntegerField(default=0)
    magic_element = models.CharField(
        max_length=10, choices=ELEMENTS_CHOICE, null=True, blank=True
    )

    def __str__(self):
        return self.name
    
class Armor(Item):
    defense = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=60)
    battle_score = models.IntegerField(default=0)
    coins = models.PositiveIntegerField(default=0)
    items = models.ManyToManyField(Item, blank=True)

    def __str__(self):
        return self.username


class Slime(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="slimes")
    name = models.CharField(max_length=60)
    magic_element = models.CharField(max_length=10, choices=ELEMENTS_CHOICE, default='NEUTRE')
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    agility = models.IntegerField(default=0)
    items = models.ManyToManyField(Item, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def weapons(self):
        """
        Retourne tous les items de type Weapon
        """
        return [item.get_real_instance() for item in self.items.all() 
                if hasattr(item, 'weapon')]

    @property
    def armors(self):
        """
        Retourne tous les items de type Armor
        """
        return [item.get_real_instance() for item in self.items.all() 
                if hasattr(item, 'armor')]

    def get_typed_items(self):
        """
        Retourne tous les items avec leur vrai type dans une liste
        """
        return [item.get_real_instance() for item in self.items.all()]
