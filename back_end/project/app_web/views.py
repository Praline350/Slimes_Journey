from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import View
from django.contrib import messages

from app_game_logic.models import *


class HomePlayerView(View):
    template_name = 'app_web/home_player.html'

    def get(self, request):
        player = Player.objects.filter(user=request.user).first()
        slimes = Slime.objects.filter(player=player).all()


        context = {
            'player': player,
            'slimes': slimes
        }
        return render(request, self.template_name, context=context)