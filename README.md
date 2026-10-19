# 🎵 Spotify Playlist Tracker

## 📋 Requirements
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (Python package and project manager)
- A [Spotify for Developers](https://developer.spotify.com/dashboard) account
- Spotify app credentials (`CLIENT_ID`, `CLIENT_SECRET`)
- The target playlist ID
---

## ⚙️ Installation
1. **Clone the repository**
```bash
git clone https://github.com/<your-username>/SpotifyScraper.git
cd SpotifyScraper
```
2. **Install dependencies**
```bash
uv sync
```
> 💡 `uv sync` reads `pyproject.toml` and `uv.lock`, creates a `.venv` virtual environment if needed, and installs the exact locked versions of the dependencies.
3. **Configure environment variables**
Create a `.env` file at the root of the project:
```env
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
ID_PLAYLIST=your_playlist_id
```
> 💡 To get a Spotify playlist ID, right-click the playlist → *Share* → *Copy link to playlist*. The ID is the string between `/playlist/` and `?`.
---

## 🚀 Usage
```bash
uv run main.py
```
On the first run, the `playlist.txt` file is created with all fetched tracks. On subsequent runs, only tracks added since the last sync are appended.
> ✅ The script now automatically paginates through the Spotify API (which returns a maximum of **100 tracks per request**) to fetch the **entire playlist**, regardless of its size — no manual offset configuration needed.
---

## 🔧 Functions
| Function | Description |
|---|---|
| `get_token()` | Obtains an access token via the Client Credentials Flow |
| `get_auth_header(token)` | Generates the Bearer authorization header |
| `get_playlist_items(token, id_playlist, offset)` | Fetches up to 100 tracks from the Spotify API, starting at `offset` |
| `get_all_playlist_items(token, id_playlist)` | Automatically paginates through `get_playlist_items()` to fetch **all** tracks of the playlist |
| `json_to_txt(items)` | Writes new tracks to `playlist.txt` |
---

## 📦 Dependencies
Dependencies are declared in `pyproject.toml` and pinned in `uv.lock`.

| Package | Usage |
|---|---|
| `requests` | HTTP requests to the Spotify API |
| `python-dotenv` | Loading environment variables |

To add a new dependency: `uv add <package>`
