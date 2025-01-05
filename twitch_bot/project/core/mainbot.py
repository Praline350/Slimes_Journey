import os
import yarl
from twitchio.ext import commands
from typing import Annotated
from twitchio.ext import commands
from dotenv import load_dotenv
from .api_twitch import *

load_dotenv()


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        self.mychannel = "QQlaPraline_"
        super().__init__(
            token=os.getenv("ACCESS_TOKEN"),
            prefix="?",
            initial_channels=[self.mychannel],
        )
        self.users_seen = set()

    def url_converter(ctx: commands.Context, arg: str) -> yarl.URL:
        return yarl.URL(arg)  # this will raise if its an invalid URL.

    async def event_message(self, message):
        if message.author is None:
            return
        print(f"{message.author.name}: {message.content}")
        # Ignore les messages du bot
        if message.echo:
            return
        try:
            if message.author.name not in self.users_seen:
                print(f"🆕 Premier message de {message.author.name}")
                self.users_seen.add(message.author.name)
                await message.channel.send(f"Bienvenue {message.author.name}!")
                print("✅ Message de bienvenue envoyé")
            else:
                print(f"ℹ️ Utilisateur déjà vu: {message.author.name}")

        except Exception as e:
            print(f"❌ ERREUR lors du traitement du message: {str(e)}")

        try:
            await self.handle_commands(message)
            print("✅ Commandes traitées")
        except Exception as e:
            print(f"❌ ERREUR lors du traitement des commandes: {str(e)}")

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

    # async def event_message(self, message):
    #     if message.author is None:
    #         return
    #     print(f"{message.author.name} : {message.content}")
    #     await super().event_message(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f"Hello {ctx.author.name}!")

    @commands.command()
    async def get_clips(self, ctx: commands.Context):
        """
        Commande pour récupérer les clips d'un streamer.
        Utilisation : ?get_clips <username>
        """
        args = ctx.message.content.split()
        if len(args) != 2:
            await ctx.send("❌ Utilisation : ?get_clips <username>")
            return

        username = args[1]
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("SECRET_CLIENT")

        try:
            # Obtenir le token d'accès
            access_token = os.getenv("ACCESS_TOKEN")

            # Récupérer l'ID du streamer
            user_id = get_user_id(username, client_id, access_token)

            # Récupérer les URLs des clips
            clips = get_clips(user_id, client_id, access_token)
            if clips:
                await ctx.send(f"🎥 Clips de {username} :")
                for clip in clips:
                    await ctx.send(clip)
                send_to_obs(clip)
            else:
                await ctx.send(f"❌ Aucun clip trouvé pour {username}.")
        except Exception as e:
            await ctx.send(f"❌ Une erreur est survenue : {e}")
