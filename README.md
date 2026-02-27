# 🎵 YT → Spotify [LIEN VERS LE SITE](https://yt-spotify-epx9w64agylxqyryydgr4f.streamlit.app)

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
## 💡 Exemple d'utilisation (Usage)

1. Lancez l'application via Streamlit.
2. Entrez vos clés API Spotify dans le menu latéral.
3. Collez l'URL d'une vidéo ou d'une playlist YouTube dans la barre de recherche.
4. Cliquez sur **"Extraire les titres"**.
5. Sélectionnez les musiques que vous souhaitez garder, puis cliquez sur **"Ajouter à Spotify"**.

## 🎧 Configuration Spotify

1. Aller sur [developer.spotify.com](https://developer.spotify.com/dashboard)
2. Créer une nouvelle app en cochant **Web API**
3. Dans Settings, ajouter le Redirect URI : `http://127.0.0.1:8888/callback`
4. Dans **User Management**, ajouter ton email Spotify
5. Copier le **Client ID** et **Client Secret** dans l'app

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

## ⚖️ Éthique & Légalité (Legal Disclaimer)

Ce projet a été développé **uniquement à des fins éducatives** dans le cadre d'un projet universitaire de Web Scraping.
- **Web Scraping responsable :** L'extraction de données sur YouTube est effectuée de manière ciblée via Selenium. Nous utilisons des délais d'attente (waits) appropriés pour ne pas surcharger les serveurs de la plateforme.
- **Transparence des données :** L'application ne collecte et ne stocke **aucune donnée personnelle**. L'authentification Spotify utilise le protocole officiel OAuth 2.0 et vos clés API (Client ID / Secret) ne sont sauvegardées sur aucun de nos serveurs.
