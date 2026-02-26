# 🎵 YT → Spotify https://yt-spotify-epx9w64agylxqyryydgr4f.streamlit.app

Un convertisseur web qui extrait les titres de vidéos ou playlists YouTube via du **web scraping** (Selenium) et les ajoute automatiquement à tes titres likés Spotify.

Projet réalisé dans le cadre d'un cours de scraping Python.

---

## 👥 Créateurs

| Nom | GitHub |
|-----|--------|
| DIB Adel | [@adeldib](https://github.com/adeldib) |
| YENER Dogukan | — |
| AIT AMROUCHE Sofiene | — |

---

## 🛠️ Stack technique

- **Python** — Langage principal
- **Streamlit** — Interface web
- **Selenium** — Web scraping YouTube
- **Spotipy** — API Spotify
- **Regex** — Nettoyage des titres

---

## ⚙️ Installation

### Prérequis
- Python 3.9+
- Google Chrome installé
- Compte Spotify Premium
- Clés API Spotify Developer

### 1. Cloner le repo

```bash
git clone https://github.com/adeldib/yt-spotify.git
cd yt-spotify
```

### 2. Créer un environnement virtuel

```bash
python -m venv env
source env/bin/activate  # Mac/Linux
env\Scripts\activate     # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l'application

```bash
streamlit run projet.py
```

---

## 🎧 Configuration Spotify

1. Va sur [developer.spotify.com](https://developer.spotify.com/dashboard)
2. Crée une nouvelle app en cochant **Web API**
3. Dans Settings, ajoute le Redirect URI : `http://127.0.0.1:8888/callback`
4. Dans **User Management**, ajoute ton email Spotify
5. Copie le **Client ID** et **Client Secret** dans l'app

---

## 🚀 Fonctionnalités

- ✅ Scraping d'une vidéo YouTube (titre + miniature)
- ✅ Scraping d'une playlist YouTube complète (lazy loading géré)
- ✅ Acceptation automatique des cookies YouTube
- ✅ Sélection individuelle des titres à ajouter
- ✅ Ajout aux titres likés Spotify
- ✅ Thème clair / sombre
- ✅ Guide d'utilisation intégré

---

## ⚠️ Limitations

- Nécessite un compte **Spotify Premium**
- Les playlists YouTube **privées** ne sont pas supportées
- L'app Spotify doit rester en **Development Mode** (max 25 utilisateurs)
