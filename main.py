import os
import base64
import sys
from requests import post, get
from dotenv import load_dotenv
from typing import Any

# Load environment variables (from a .env file)
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
    Requests an access token using the client_id and client_secret
    provided by the environment.

    :return: The token used to make requests to the API.
    """
    try:
        auth_string = f"{client_id}:{client_secret}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            # The space after Basic is required!
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
    Builds the request header.

    :param token: Token used to authenticate the request
    :return: The request header
    """
    return {"Authorization": "Bearer " + token}


def get_playlist_items(token: str, id_playlist: str, offset: int = 0) -> Any:
    """
    Sends a request to the Spotify API to get the list of tracks in the
    given playlist.
    The request fetches at most 100 tracks. Make sure to set the offset
    accordingly.

    :param token: Token used to authenticate the request
    :param id_playlist: Playlist ID
    :param offset: Index from which tracks are fetched

    :return: The fetched tracks, in JSON format
    """
    url = "https://api.spotify.com/v1/playlists/" + id_playlist + \
        ("/items?fields=items%28added_at%2C+item%28name%2C+artists%28name%29"
         "%29%29&offset=") + str(offset)
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    result.raise_for_status()
    json_result = result.json()

    # To get the result in a JSON file instead:
    # with open("playlist.json", "w", encoding="utf-8") as f:
    #    json.dump(json_result, f, indent=4)
    return json_result


def get_all_playlist_items(token: str, id_playlist: str) -> Any:
    """
    Fetches all the tracks of a playlist by automatically paginating in
    chunks of 100 (the maximum limit enforced by the Spotify API).

    :param token: Token used to authenticate the request
    :param id_playlist: Playlist ID

    :return: The complete list of fetched tracks, in JSON format
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
    Writes to playlist.txt the tracks whose added date is later than the
    last track added to the file.

    :param items: The JSON list of tracks obtained from the request.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, "playlist.txt")
    n = len(items["items"])

    if not os.path.isfile(filename):
        print("Starting first write.")
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
            s += f"\nLast addition date:\n{last_added_at}"
            f.write(s)
            print("First write complete.")
    else:
        with open(filename, "r") as f:
            lines = f.readlines()
            last_line = lines[len(lines) - 1]

        if (last_line < items["items"][n - 1]["added_at"]):
            print("Starting write.")
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
                s += f"\nLast addition date:\n{last_added_at}"
                f.write(s)
                print("Write complete.")
                print(f"{nb_added} tracks added.")
        else:
            print("No tracks to add to the file.")


if __name__ == "__main__":
    token = get_token()
    print("Request in progress...")
    items = get_all_playlist_items(token, id_playlist)
    json_to_txt(items)
