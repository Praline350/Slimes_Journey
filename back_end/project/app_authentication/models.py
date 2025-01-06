from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    twitch_id = models.CharField(max_length=50, blank=True, null=True)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    token_expires = models.DateTimeField(blank=True, null=True)


class Streamer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.channel_name = self.user.username
        super(Streamer, self).save(*args, **kwargs)

    def __str__(self):
        return self.channel_name
