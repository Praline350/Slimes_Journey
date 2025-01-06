from django.contrib import admin
from .models import Player, Slime, Item


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = [
        "username",
    ]


@admin.register(Slime)
class SlimeAdmin(admin.ModelAdmin):
    list_display = ["name", "player"]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
