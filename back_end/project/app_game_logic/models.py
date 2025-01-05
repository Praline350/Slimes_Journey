from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

ELEMENTS_CHOICE = [("EAU", "Eau"), ("FEU", "Feu"), ("AIR", "Air"), ("TERRE", "Terre")]
ITEMS_TYPE_CHOICE = [("ARME", "Arme"), ("ARMURE", "Armure")]
SKILL_TYPE_CHOICE = [("ACTIVE", "Active"), ("PASSIVE", "Passive")]


class Item(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(null=True, blank=True)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    agility = models.IntegerField(default=0)
    magic_element = models.CharField(
        max_length=10, choices=ELEMENTS_CHOICE, null=True, blank=True
    )
    type = models.CharField(max_length=15, choices=ITEMS_TYPE_CHOICE)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    type = models.CharField(max_length=15, choices=SKILL_TYPE_CHOICE)


class Player(models.Model):
    username = models.CharField(max_length=60)
    battle_score = models.IntegerField(default=0)
    coins = models.PositiveIntegerField(default=0)
    items = models.ManyToManyField(Item, blank=True)

    def __str__(self):
        return self.username


class Slime(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="slimes")
    name = models.CharField(max_length=60)
    magic_element = models.CharField(max_length=10, choices=ELEMENTS_CHOICE)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    agility = models.IntegerField(default=0)
    items = models.ManyToManyField(Item, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.name
