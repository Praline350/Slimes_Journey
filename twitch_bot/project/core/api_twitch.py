import os
from dotenv import load_dotenv
from obswebsocket import obsws, requests
import requests

load_dotenv()

# Connexion WebSocket OBS
OBS_HOST = "localhost"  # Adresse du serveur OBS
OBS_PORT = 4455  # Port WebSocket d'OBS
OBS_PASSWORD = os.getenv("OBS_PASSWORD")  # Mot de passe configuré dans OBS


def send_to_obs(url):
    """Met à jour l'URL d'une source navigateur."""
    try:
        # Connexion à OBS WebSocket
        client = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
        client.connect()
        print("✅ Connecté à OBS WebSocket")

        # Mettre à jour l'URL de la source
        response = client.call(
            requests.SetSourceSettings(
                sourceName="TwitchClip",  # Nom de la source navigateur dans OBS
                sourceSettings={"url": url},  # Nouvel URL
                overlay=True,  # Applique les changements en surcouche
            )
        )
        print(f"✅ URL mise à jour avec succès : {response}")

    except Exception as e:
        print(f"❌ Erreur : {e}")

    finally:
        # Déconnexion propre
        client.disconnect()
        print("✅ Déconnecté d'OBS WebSocket")


def get_user_id(username, client_id, access_token):
    url = f"https://api.twitch.tv/helix/users"
    headers = {"Client-ID": client_id, "Authorization": f"Bearer {access_token}"}
    params = {"login": username}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    if data["data"]:
        return data["data"][0]["id"]
    else:
        raise ValueError("Utilisateur introuvable")


def get_clips(user_id, client_id, access_token):
    url = f"https://api.twitch.tv/helix/clips"
    headers = {"Client-ID": client_id, "Authorization": f"Bearer {access_token}"}
    params = {"broadcaster_id": user_id, "first": 1}  # Récupère le clip le plus récent
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    if data["data"]:
        return [clip["url"] for clip in data["data"]]
    else:
        return []
