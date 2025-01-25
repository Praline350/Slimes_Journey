from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

ELEMENTS_CHOICE = [
    ("FLAMME", "Flamme"),
    ("VAGUE", "Vague"),
    ("OMBRE", "Ombre"),
    ("LUMIERE", "Lumière"),
    ("METAUX", "Métaux"),
    ("ETHERE", "Éthéré"),
    ("TEMPESTE", "Tempête"),
    ("ECHO", "Echo"),
    ("FUSION", "Fusion")
]
ITEMS_TYPE_CHOICE = [("ARME", "Arme"), ("ARMURE", "Armure")]
SKILL_TYPE_CHOICE = [("ACTIVE", "Active"), ("PASSIVE", "Passive")]
EFFECT_TYPE_CHOICE = [
    ("POISON", "Poison"),
    ("STUN", "Stun"),
    ("BURN", "Burn"),
    ("FREEZE", "Freeze"),
    ("ELECTROCUTE", "Electrocute"),
    ("HEAL", "Heal"),
    ("BUFF", "Buff"),
    ("DEBUFF", "Debuff"),
]


class Skill(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    type = models.CharField(max_length=15, choices=SKILL_TYPE_CHOICE)

class SkillEffect(models.Model):
    skill = models.ForeignKey(Skill, related_name="effects", on_delete=models.CASCADE)
    effect_type = models.CharField(max_length=15, choices=EFFECT_TYPE_CHOICE)
    power = models.FloatField(help_text="Strength of the effect, e.g., poison damage per turn.")
    duration = models.IntegerField(help_text="Duration in turns for the effect.", null=True, blank=True)
    chance = models.FloatField(default=1.0, help_text="Chance (0.0 to 1.0) for the effect to apply.")

class Item(models.Model):
    name = models.CharField(max_length=60)
    type = models.CharField(max_length=50, choices=ITEMS_TYPE_CHOICE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    magic_element = models.CharField(max_length=10, choices=ELEMENTS_CHOICE, default='NEUTRE')
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    magic_attack = models.IntegerField(default=0)
    magic_defense = models.IntegerField(default=0)
    agility = models.IntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=60)
    battle_score = models.IntegerField(default=0)
    coins = models.PositiveIntegerField(default=0)
    items = models.ManyToManyField(Item, through="Inventory")

    def __str__(self):
        return self.username


class Slime(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="slimes")
    name = models.CharField(max_length=60)
    in_active_team = models.BooleanField(default=False)
    is_fighter = models.BooleanField(default=False)
    max_hp = models.PositiveIntegerField(default=20)
    hp = models.IntegerField(default=20)
    magic_element = models.CharField(max_length=10, choices=ELEMENTS_CHOICE, default='NEUTRE')
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    magic_attack = models.IntegerField(default=0)
    magic_defense = models.IntegerField(default=0)
    agility = models.IntegerField(default=0)
    items = models.ManyToManyField(Item, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Si ce slime est défini comme 'is_fighter'
        if self.is_fighter:
            # Passer tous les autres slimes du même joueur à `is_fighter=False`
            Slime.objects.filter(player=self.player, is_fighter=True).exclude(id=self.id).update(is_fighter=False)
        super().save(*args, **kwargs)  # Appeler la méthode save normale
        

class Inventory(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # Quantité d'item

    class Meta:
        unique_together = ('player', 'item')  # Un couple slime-item unique

    def __str__(self):
        return f"{self.quantity}x {self.item.name} (player: {self.player.username})"


