# 🎵 Spotify Playlist Tracker

Un script Python qui interroge l'API Spotify pour récupérer les morceaux d'une playlist et les exporte dans un fichier `.txt`, en ne rajoutant que les nouvelles musiques ajoutées depuis la dernière synchronisation.

---

## 📋 Prérequis

- Python 3.10+
- Un compte [Spotify for Developers](https://developer.spotify.com/dashboard)
- Les identifiants d'une application Spotify (`CLIENT_ID`, `CLIENT_SECRET`)
- L'ID de la playlist cible

---

## ⚙️ Installation

1. **Cloner le dépôt**

```bash
git clone https://github.com/<your-username>/SpotifyScraper.git
cd spotify-playlist-tracker
```

2. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

3. **Configurer les variables d'environnement**

Créer un fichier `.env` à la racine du projet :

```env
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
ID_PLAYLIST=your_playlist_id
```

> 💡 Pour obtenir l'ID d'une playlist Spotify, faire un clic droit sur la playlist → *Partager* → *Copier le lien de la playlist*. L'ID est la chaîne de caractères entre `/playlist/` et `?`.

---

## 🚀 Utilisation

```bash
python main.py
```

À la première exécution, le fichier `playlist.txt` est créé avec tous les morceaux récupérés. Aux exécutions suivantes, seuls les morceaux ajoutés après la dernière synchronisation sont ajoutés.

> ⚠️ L'API Spotify retourne au maximum **100 morceaux par requête**. L'offset dans `get_playlist_tracks()` peut être ajusté directement dans le `__main__` selon la taille de la playlist.

---

## 🔧 Fonctions

| Fonction | Description |
|---|---|
| `get_token()` | Obtient un token d'accès via les credentials Client Credentials Flow |
| `get_auth_header(token)` | Génère le header d'autorisation Bearer |
| `get_playlist_tracks(token, id_playlist, offset)` | Récupère jusqu'à 100 morceaux depuis l'API Spotify |
| `json_to_txt(items)` | Écrit les nouveaux morceaux dans `playlist.txt` |

---

## 📦 Dépendances

| Package | Usage |
|---|---|
| `requests` | Requêtes HTTP vers l'API Spotify |
| `python-dotenv` | Chargement des variables d'environnement |
