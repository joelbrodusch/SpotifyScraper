# 🎵 Spotify Playlist Tracker
A Python script that queries the Spotify API to fetch the tracks of a playlist and exports them to a `.txt` file, only appending new songs added since the last sync.

---

## 📋 Requirements
- Python 3.10+
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
pip install -r requirements.txt
```
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
python main.py
```
On the first run, the `playlist.txt` file is created with all fetched tracks. On subsequent runs, only tracks added since the last sync are appended.
> ⚠️ The Spotify API returns a maximum of **100 tracks per request**. The offset in `get_playlist_tracks()` can be adjusted directly in `__main__` depending on the playlist size.
---

## 🔧 Functions
| Function | Description |
|---|---|
| `get_token()` | Obtains an access token via the Client Credentials Flow |
| `get_auth_header(token)` | Generates the Bearer authorization header |
| `get_playlist_tracks(token, id_playlist, offset)` | Fetches up to 100 tracks from the Spotify API |
| `json_to_txt(items)` | Writes new tracks to `playlist.txt` |
---

## 📦 Dependencies
| Package | Usage |
|---|---|
| `requests` | HTTP requests to the Spotify API |
| `python-dotenv` | Loading environment variables |
 
