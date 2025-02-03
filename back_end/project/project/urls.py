
from django.contrib import admin
from django.urls import path

from app_web.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePlayerView.as_view(), name='home_player')
]
