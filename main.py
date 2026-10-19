import os
import base64
import sys
from requests import post, get
from dotenv import load_dotenv
from typing import Any

# Charge les variables d'environnement (d'un fichier .env)
try:
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    id_playlist = os.getenv("ID_PLAYLIST")
    if not client_id or not client_secret or not id_playlist:
        raise Exception("Missing variables in .env")
except Exception as e:
    print(e)
    sys.exit()


def get_token() -> str:
    """
    Exécute une demande de token grâce au client_id et au client_secret fournit par l'environnement.

    :return: Le token pour faire la requête à l'API.
    """
    try:
        auth_string = f"{client_id}:{client_secret}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            # L'espace après Basic est nécessaire !
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        result.raise_for_status()
        json_result = result.json()
        token = str(json_result["access_token"])
        return token
    except Exception as e:
        print(e)
        sys.exit()


def get_auth_header(token: str) -> dict[str, str]:
    """
    Crée le header de la requête.
    :param token: Token qui permet de réaliser la requête
    :return: Le header de la requête
    """
    return {"Authorization": "Bearer " + token}


def get_playlist_items(token: str, id_playlist: str, offset: int = 0) -> Any:
    """
    Effectue la requête via l'API de Spotify pour obtenir la liste des musiques dans la playlist passée en paramètre.
    La requête extrait au maximum 100 musiques. Attention à bien calibrer l'offset en conséquence.

    :param token: Token qui permet de réaliser la requête
    :param id_playlist: ID de la playlist
    :param offset: Index à partir duquel les musiques sont scrapées

    :return: La liste des musiques scrapées sour format JSON
    """
    url = "https://api.spotify.com/v1/playlists/" + id_playlist + \
        "/items?fields=items%28added_at%2C+item%28name%2C+artists%28name%29%29%29&offset=" + str(offset)
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    result.raise_for_status()
    json_result = result.json()

    # Si on souhaite avoir le résultat dans un fichier JSON :
    # with open("playlist.json", "w", encoding="utf-8") as f:
    #    json.dump(json_result, f, indent=4)
    return json_result


def get_all_playlist_items(token: str, id_playlist: str) -> Any:
    """
    Récupère la totalité des musiques d'une playlist en paginant automatiquement
    par tranches de 100 (limite maximale imposée par l'API Spotify).

    :param token: Token qui permet de réaliser la requête
    :param id_playlist: ID de la playlist

    :return: La liste complète des musiques scrapées, au format JSON
    """
    page_size = 100
    offset = 0
    all_items: list[Any] = []

    while True:
        page = get_playlist_items(token, id_playlist, offset)
        page_items = page.get("items", [])
        all_items.extend(page_items)

        if len(page_items) < page_size:
            break
        offset += page_size

    return {"items": all_items}


def json_to_txt(items: Any) -> None:
    """
    Écrit dans le fichier playlist.txt les musiques dont leurs dates d'ajout est postérieure à la dernière musique
    ajoutée au fichier.

    :param items: La liste JSON des musiques acquises par la requête.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, "playlist.txt")
    n = len(items["items"])

    if not os.path.isfile(filename):
        print("Début de la première écriture.")
        with open(filename, "w") as f:
            s = ""
            for track in items["items"]:
                artists = track["item"]["artists"]
                n_artists = len(artists)
                for i, artist in enumerate(artists):
                    sep = " " if i == n_artists - 1 else ", "
                    s += artist["name"] + sep
                s += "— " + track["item"]["name"] + "\n\n"
            last_added_at = items["items"][n - 1]["added_at"]
            s += f"\nDate du dernier ajout :\n{last_added_at}"
            f.write(s)
            print("Fin de la première écriture.")
    else:
        with open(filename, "r") as f:
            lines = f.readlines()
            last_line = lines[len(lines) - 1]

        if (last_line < items["items"][n - 1]["added_at"]):
            print("Début d'écriture.")
            with open(filename, "w") as f:
                s = ""
                nb_added = 0
                for track in items["items"]:
                    if (last_line < track["added_at"]):
                        nb_added += 1
                        artists = track["item"]["artists"]
                        n_artists = len(artists)
                        for i, artist in enumerate(artists):
                            sep = " " if i == n_artists - 1 else ", "
                            s += artist["name"] + sep
                        s += "— " + track["item"]["name"] + "\n\n"
                last_added_at = items["items"][n - 1]["added_at"]
                s += f"\nDate du dernier ajout :\n{last_added_at}"
                f.write(s)
                print("Fin d'écriture.")
                print(f"{nb_added} musiques ont été ajoutées.")
        else:
            print("Aucune musique à rajouter au fichier.")


if __name__ == "__main__":
    token = get_token()
    print("Requête en cours...")
    items = get_all_playlist_items(token, id_playlist)
    json_to_txt(items)
