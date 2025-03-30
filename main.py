import os
import base64
import json
from requests import post, get
from dotenv import load_dotenv

# Charge les variables d'environnement (d'un fichier .env)
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    """
    Exécute une demande de token grâce au client_id et au client_secret fournit par l'environnement.
    :return: Le token pour faire la requête à l'API.
    """
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url ="https://accounts.spotify.com/api/token"
    headers = {
        # L'espace après Basic est nécessaire !
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    """
    Crée le header de la requête.
    :param token: Token qui permet de réaliser la requête
    :return: Le header de la requête
    """
    return {"Authorization": "Bearer " + token}

def get_playlist_tracks(token, id_playlist, offset=None):
    """
    Effectue la requête via l'API de Spotify pour obtenir la liste des musiques dans la playlist passée en paramètre.
    La requête extraie au maximum 100 musiques. Attention à bien calibrer l'offset en conséquence.
    :param token: Token qui permet de réaliser la requête
    :param id_playlist: ID de la playlist
    :param offset: Index à partir duquel les musiques sont scrapées
    :return: La liste des musiques scrapées sour format JSON
    """
    if offset is None:
        offset = 0
    url = "https://api.spotify.com/v1/playlists/" + id_playlist + "/tracks?fields=items%28added_at%2Ctrack%28name%2Cartists%28name%29%29%29&offset=" + str(offset)
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    # Si on souhaite avoir le résultat dans un fichier JSON :
    # with open("playlist.json", "w", encoding="utf-8") as f:
    #    json.dump(json_result, f, indent=4)

    return json_result

def json_to_txt(items):
    """
    Écrit dans le fichier playlist.txt les musiques dont leurs dates d'ajout est postérieure à la dernière musique
    ajoutée au fichier.
    :param items: La liste JSON des musiques acquises par la requête.
    """
    filename = "playlist.txt"
    n = len(items["items"])

    if not os.path.isfile(filename):
        print("Début de la première écriture.")
        with open(filename, "w") as f:
            s = ""
            for item in items["items"]:
                for artist in item["track"]["artists"]:
                    if len(item["track"]["artists"]) > 1:
                        s += artist["name"] + ", "
                    else:
                        s += artist["name"] + " "
                s += "— " + item["track"]["name"] + "\n"
            s += "\nDate du dernier ajout :\n" + items["items"][n-1]["added_at"]
            f.write(s)
            print("Fin de la première écriture.")
    else:
        with open(filename, "r") as f:
            lines = f.readlines()
            last_line = lines[len(lines)-1]

        if (last_line < items["items"][n-1]["added_at"]):
            print("Début d'écriture.")
            with open(filename, "w") as f:
                s = ""
                for item in items["items"]:
                    if (last_line < item["added_at"]):
                        for artist in item["track"]["artists"]:
                            if len(item["track"]["artists"]) > 1:
                                s += artist["name"] + ", "
                            else:
                                s += artist["name"] + " "
                        s += "— " + item["track"]["name"] + "\n"
                s += "\nDate du dernier ajout :\n" + items["items"][n - 1]["added_at"]
                f.write(s)
                print("Fin d'écriture.")
                print(str(len(lines) - 2) + " musiques ont été ajoutées.")
        else:
            print("Aucune musique à rajouter au fichier.")

# Main
id_playlist = "4sX65t1XzJjbQcZVNBV74f"
token = get_token()

print("Requête en cours...")
items = get_playlist_tracks(token, id_playlist, 240)
json_to_txt(items)
