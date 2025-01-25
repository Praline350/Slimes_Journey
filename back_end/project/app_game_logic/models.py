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
    magic_attack = models.IntegerField(default=0)
    magic_element = models.CharField(
        max_length=10, choices=ELEMENTS_CHOICE, null=True, blank=True
    )

    def __str__(self):
        return self.name
    
class Armor(Item):
    defense = models.IntegerField(default=0)
    magic_defense = models.IntegerField(default=0)

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
    items = models.ManyToManyField(Item, through='SlimeItem')
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Si ce slime est défini comme 'is_fighter'
        if self.is_fighter:
            # Passer tous les autres slimes du même joueur à `is_fighter=False`
            Slime.objects.filter(player=self.player, is_fighter=True).exclude(id=self.id).update(is_fighter=False)
        super().save(*args, **kwargs)  # Appeler la méthode save normale
        
    @property
    def weapons(self):
        """
        Retourne les armes avec leur quantité.
        """
        return [
            (slime_item.item.get_real_instance(), slime_item.quantity)
            for slime_item in SlimeItem.objects.filter(slime=self, item__weapon__isnull=False)
        ]

    @property
    def armors(self):
        """
        Retourne les armures avec leur quantité.
        """
        return [
            (slime_item.item.get_real_instance(), slime_item.quantity)
            for slime_item in SlimeItem.objects.filter(slime=self, item__armor__isnull=False)
        ]

    def get_typed_items(self):
        """
        Retourne tous les items avec leur vrai type et leur quantité.
        """
        return [
            (slime_item.item.get_real_instance(), slime_item.quantity)
            for slime_item in SlimeItem.objects.filter(slime=self)
        ]
    

class SlimeItem(models.Model):
    slime = models.ForeignKey(Slime, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # Quantité d'item
    is_equipped = models.BooleanField(default=False)

    class Meta:
        unique_together = ('slime', 'item')  # Un couple slime-item unique

    def __str__(self):
        return f"{self.quantity}x {self.item.name} (Slime: {self.slime.name})"

    @property
    def weapons(self):
        """
        Retourne l'arme si l'item est une instance de Weapon.
        """
        item_instance = self.item.get_real_instance()
        if isinstance(item_instance, Weapon):
            return item_instance
        return None

    @property
    def armors(self):
        """
        Retourne l'armure si l'item est une instance de Armor.
        """
        item_instance = self.item.get_real_instance()
        if isinstance(item_instance, Armor):
            return item_instance
        return None
    
    @classmethod
    def get_equipped_items(cls, slime):
        """
        Retourne tous les items équipés pour un slime donné.
        """
        return cls.objects.filter(slime=slime, is_equipped=True)

