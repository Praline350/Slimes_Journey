from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import View
from django.contrib import messages


class HomePlayerView(View):
    template_name = 'app_web/home_player.html'

    def get(self, request):
        return render(request, self.template_name)