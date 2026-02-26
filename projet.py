import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==========================================
# CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="YouTube → Spotify",
    page_icon="🎵",
    layout="wide"
)

# ==========================================
# THÈME : CLAIR / SOMBRE
# ==========================================
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = True
if "page" not in st.session_state:
    st.session_state["page"] = "convertisseur"

dark = st.session_state["dark_mode"]

if dark:
    bg          = "#0a0a0a"
    bg2         = "#141414"
    bg3         = "#1a1a1a"
    sidebar_bg  = "#111111"
    border      = "#222"
    border2     = "#333"
    text        = "#ffffff"
    text2       = "#aaaaaa"
    text3       = "#555555"
    divider_col = "#1e1e1e"
    check_col   = "#cccccc"
    toggle_icon = "☀️"
    toggle_label= "Mode clair"
    success_bg  = "#0d1f14"
    nav_active  = "#1DB954"
    nav_active_bg = "rgba(29,185,84,0.12)"
    nav_hover   = "rgba(255,255,255,0.05)"
    step_bg     = "#141414"
    step_border = "#222"
    warn_bg     = "#1a1200"
    warn_border = "#554400"
    warn_text   = "#ffcc00"
else:
    bg          = "#f5f5f5"
    bg2         = "#ffffff"
    bg3         = "#eeeeee"
    sidebar_bg  = "#ffffff"
    border      = "#dddddd"
    border2     = "#cccccc"
    text        = "#111111"
    text2       = "#444444"
    text3       = "#888888"
    divider_col = "#dddddd"
    check_col   = "#222222"
    toggle_icon = "🌙"
    toggle_label= "Mode sombre"
    success_bg  = "#e8f8ee"
    nav_active  = "#1DB954"
    nav_active_bg = "rgba(29,185,84,0.10)"
    nav_hover   = "rgba(0,0,0,0.04)"
    step_bg     = "#ffffff"
    step_border = "#e0e0e0"
    warn_bg     = "#fffbe6"
    warn_border = "#ffe58f"
    warn_text   = "#7a5c00"

# ==========================================
# CSS GLOBAL
# ==========================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    .stApp {{
        background: {bg} !important;
        font-family: 'DM Sans', sans-serif;
    }}

    #MainMenu, footer {{visibility: hidden;}}

    .block-container {{
        background: {bg} !important;
        padding-top: 2rem !important;
        max-width: 780px !important;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: {sidebar_bg} !important;
        border-right: 1px solid {border} !important;
    }}

    [data-testid="stSidebar"] > div {{
        padding: 1.5rem 1rem !important;
    }}

    .sidebar-logo {{
        font-family: 'Syne', sans-serif;
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF0000 0%, #ff4444 40%, #1DB954 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2rem;
    }}

    .sidebar-tagline {{
        color: {text3};
        font-size: 0.72rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }}

    .nav-section-label {{
        color: {text3};
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        margin-top: 1.2rem;
        padding-left: 0.5rem;
    }}

    .nav-item {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.55rem 0.75rem;
        border-radius: 10px;
        cursor: pointer;
        color: {text2};
        font-size: 0.9rem;
        font-family: 'DM Sans', sans-serif;
        margin-bottom: 0.2rem;
        transition: all 0.15s ease;
        text-decoration: none;
    }}

    .nav-item:hover {{
        background: {nav_hover};
        color: {text};
    }}

    .nav-item.active {{
        background: {nav_active_bg};
        color: {nav_active};
        font-weight: 500;
    }}

    .sidebar-divider {{
        border: none;
        border-top: 1px solid {border};
        margin: 1.2rem 0;
    }}

    .sidebar-footer {{
        color: {text3};
        font-size: 0.7rem;
        text-align: center;
        margin-top: 2rem;
        opacity: 0.5;
    }}

    /* Titre principal */
    .main-title {{
        font-family: 'Syne', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF0000 0%, #ff4444 40%, #1DB954 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }}

    .subtitle {{
        color: {text3};
        text-align: center;
        font-size: 0.95rem;
        font-weight: 300;
        margin-bottom: 2rem;
    }}

    /* Page titre */
    .page-title {{
        font-family: 'Syne', sans-serif;
        font-size: 1.6rem;
        font-weight: 800;
        color: {text};
        margin-bottom: 0.3rem;
    }}

    .page-subtitle {{
        color: {text3};
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }}

    /* Input */
    .stTextInput > div > div > input {{
        background: {bg3} !important;
        border: 1px solid {border2} !important;
        border-radius: 12px !important;
        color: {text} !important;
        font-family: 'DM Sans', sans-serif !important;
        padding: 0.8rem 1rem !important;
        font-size: 0.95rem !important;
    }}

    .stTextInput > div > div > input:focus {{
        border-color: #1DB954 !important;
        box-shadow: 0 0 0 2px rgba(29, 185, 84, 0.15) !important;
    }}

    .stTextInput > div > div > input::placeholder {{
        color: {text3} !important;
    }}

    .stTextInput label {{
        color: {text3} !important;
        font-size: 0.8rem !important;
    }}

    /* Boutons */
    .stButton > button {{
        background: linear-gradient(135deg, #1DB954, #17a349) !important;
        color: #000 !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.65rem 2rem !important;
        width: 100% !important;
        letter-spacing: 0.05em !important;
        transition: all 0.2s ease !important;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(29, 185, 84, 0.35) !important;
    }}

    /* Checkbox */
    .stCheckbox label {{
        color: {check_col} !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.9rem !important;
    }}

    /* Expander */
    .streamlit-expanderHeader {{
        background: {bg2} !important;
        color: {text2} !important;
        border: 1px solid {border} !important;
        border-radius: 12px !important;
    }}

    .streamlit-expanderContent {{
        background: {bg2} !important;
        border: 1px solid {border} !important;
        border-top: none !important;
    }}

    /* Divider */
    .divider {{
        border: none;
        border-top: 1px solid {divider_col};
        margin: 1.5rem 0;
    }}

    /* Step card (page guide) */
    .step-card {{
        background: {step_bg};
        border: 1px solid {step_border};
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        display: flex;
        gap: 1rem;
        align-items: flex-start;
    }}

    .step-number {{
        background: linear-gradient(135deg, #1DB954, #17a349);
        color: #000;
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 0.85rem;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        margin-top: 2px;
    }}

    .step-content h4 {{
        color: {text};
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 0.95rem;
        margin: 0 0 0.3rem 0;
    }}

    .step-content p {{
        color: {text2};
        font-size: 0.85rem;
        margin: 0;
        line-height: 1.5;
    }}

    .step-content code {{
        background: {bg3};
        color: #1DB954;
        padding: 0.1rem 0.4rem;
        border-radius: 4px;
        font-size: 0.8rem;
    }}

    .warn-box {{
        background: {warn_bg};
        border: 1px solid {warn_border};
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 1.5rem;
        color: {warn_text};
        font-size: 0.87rem;
        line-height: 1.5;
    }}

    .info-box {{
        background: {nav_active_bg};
        border: 1px solid rgba(29,185,84,0.25);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 1.5rem;
        color: {text2};
        font-size: 0.87rem;
        line-height: 1.5;
    }}

    .playlist-header {{
        font-family: 'Syne', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: {text};
        margin-bottom: 0.3rem;
    }}

    .playlist-count {{
        color: {text3};
        font-size: 0.8rem;
        margin-bottom: 1rem;
    }}

</style>
""", unsafe_allow_html=True)


# ==========================================
# CLASSES MÉTIER
# ==========================================
class YoutubeScraper:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--mute-audio')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    def _accept_cookies(self, driver):
        try:
            wait = WebDriverWait(driver, 5)
            cookie_btn = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                '//button[contains(., "Tout accepter") or contains(., "Accept all") or contains(., "Accepter tout")]'
            )))
            cookie_btn.click()
            time.sleep(1)
        except:
            pass

    def is_playlist(self, url):
        return "playlist?list=" in url

    def get_single_video(self, url):
        driver = webdriver.Chrome(options=self.options)
        try:
            driver.get(url)
            self._accept_cookies(driver)
            wait = WebDriverWait(driver, 10)
            meta_title = wait.until(EC.presence_of_element_located((By.XPATH, '//meta[@property="og:title"]')))
            raw_title = meta_title.get_attribute("content")
            clean_title = re.sub(r'\[.*?\]', '', raw_title)
            clean_title = re.sub(r'\(.*?\)', '', clean_title).strip()
            try:
                meta_thumb = driver.find_element(By.XPATH, '//meta[@property="og:image"]')
                thumbnail = meta_thumb.get_attribute("content")
            except:
                thumbnail = None
            return [{"title": clean_title, "raw_title": raw_title, "thumbnail": thumbnail}]
        except:
            return []
        finally:
            driver.quit()

    def get_playlist_videos(self, url):
        driver = webdriver.Chrome(options=self.options)
        try:
            driver.get(url)
            self._accept_cookies(driver)
            wait = WebDriverWait(driver, 15)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "ytd-playlist-video-renderer")))
            try:
                playlist_title = driver.find_element(By.CSS_SELECTOR, "h1.title yt-formatted-string").text
            except:
                try:
                    playlist_title = driver.find_element(By.CSS_SELECTOR, "yt-formatted-string.style-scope.yt-dynamic-sizing-formatted-string").text
                except:
                    playlist_title = "Playlist YouTube"
            last_count = 0
            for _ in range(30):
                items = driver.find_elements(By.TAG_NAME, "ytd-playlist-video-renderer")
                if len(items) == last_count:
                    break
                last_count = len(items)
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(1.5)
            videos = []
            for item in driver.find_elements(By.TAG_NAME, "ytd-playlist-video-renderer"):
                try:
                    title_el = item.find_element(By.CSS_SELECTOR, "#video-title")
                    raw_title = title_el.get_attribute("title") or title_el.text
                    if not raw_title:
                        continue
                    clean_title = re.sub(r'\[.*?\]', '', raw_title)
                    clean_title = re.sub(r'\(.*?\)', '', clean_title).strip()
                    try:
                        thumb = item.find_element(By.CSS_SELECTOR, "img.yt-core-image")
                        thumbnail = thumb.get_attribute("src")
                    except:
                        thumbnail = None
                    videos.append({"title": clean_title, "raw_title": raw_title, "thumbnail": thumbnail})
                except:
                    continue
            return playlist_title, videos
        except:
            return None, []
        finally:
            driver.quit()


class SpotifyManager:
    def __init__(self, client_id, client_secret):
        os.environ["SPOTIPY_CLIENT_ID"] = client_id
        os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
        os.environ["SPOTIPY_REDIRECT_URI"] = "http://127.0.0.1:8888/callback"
        scope = "user-library-modify"
        try:
            auth_manager = SpotifyOAuth(scope=scope, cache_path=".cache_victoire", show_dialog=True)
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            self.sp.current_user()
            self.connected = True
        except Exception as e:
            self.connected = False
            self.error = str(e)

    def search_track(self, song_name):
        try:
            results = self.sp.search(q=song_name, type='track', limit=1)
            items = results.get('tracks', {}).get('items', [])
            if not items:
                return None
            track = items[0]
            return {
                "uri": f"spotify:track:{track['id']}",
                "name": track['name'],
                "artist": track['artists'][0]['name'],
                "cover": track['album']['images'][0]['url'] if track['album']['images'] else None
            }
        except:
            return None

    def add_to_favorites(self, track_uri):
        self.sp._put(f"me/library?uris={track_uri}")


# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown('<div class="sidebar-logo">YT → Spotify</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-tagline">Convertisseur YouTube · Spotify</div>', unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div class="nav-section-label">Navigation</div>', unsafe_allow_html=True)

    # Nav items
    pages = [
        ("convertisseur", "🎵", "Convertisseur"),
        ("guide", "📖", "Comment utiliser"),
        ("about", "👥", "À propos"),
    ]

    for page_id, icon, label in pages:
        active_class = "active" if st.session_state["page"] == page_id else ""
        if st.button(f"{icon}  {label}", key=f"nav_{page_id}"):
            st.session_state["page"] = page_id
            st.rerun()

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # Toggle thème dans la sidebar
    st.markdown('<div class="nav-section-label">Apparence</div>', unsafe_allow_html=True)
    if st.button(f"{toggle_icon}  {toggle_label}"):
        st.session_state["dark_mode"] = not st.session_state["dark_mode"]
        st.rerun()

    st.markdown(f'<div class="sidebar-footer">Made with Streamlit · Selenium · Spotipy</div>', unsafe_allow_html=True)


# ==========================================
# PAGE : CONVERTISSEUR
# ==========================================
if st.session_state["page"] == "convertisseur":

    st.markdown('<div class="main-title">YT → Spotify</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">Vidéo ou playlist YouTube · Choisis les titres · C\'est ajouté</div>', unsafe_allow_html=True)

    with st.expander("⚙️  Configuration Spotify", expanded=not st.session_state.get("spotify_configured", False)):
        col1, col2 = st.columns(2)
        with col1:
            client_id_input = st.text_input("Client ID", type="password", placeholder="75f622f83ffc...")
        with col2:
            client_secret_input = st.text_input("Client Secret", type="password", placeholder="4d47a1cfd9a4...")

        if st.button("🔗 Connecter Spotify"):
            if client_id_input and client_secret_input:
                with st.spinner("Connexion à Spotify..."):
                    spotify_test = SpotifyManager(client_id_input, client_secret_input)
                    if spotify_test.connected:
                        st.session_state["spotify_configured"] = True
                        st.session_state["client_id"] = client_id_input
                        st.session_state["client_secret"] = client_secret_input
                        st.success("✅ Connecté à Spotify !")
                    else:
                        st.error("❌ Connexion échouée. Vérifie tes clés API.")
            else:
                st.warning("Remplis les deux champs.")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    if not st.session_state.get("spotify_configured", False):
        st.markdown(
            f'<div style="text-align:center; color:{text3}; font-size:0.9rem; padding: 2rem 0;">'
            'Configure d\'abord ta connexion Spotify ci-dessus 👆<br>'
            f'<span style="font-size:0.8rem;">Tu ne sais pas comment faire ? Consulte la section <b>📖 Comment utiliser</b> dans la barre de gauche.</span>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        url_input = st.text_input(
            "Lien YouTube",
            placeholder="Vidéo : youtube.com/watch?v=...   ou   Playlist : youtube.com/playlist?list=...",
            label_visibility="collapsed"
        )

        scraper = YoutubeScraper()

        if st.button("🔍 Analyser le lien"):
            if not url_input:
                st.warning("Colle d'abord un lien YouTube !")
            elif "youtube.com" not in url_input and "youtu.be" not in url_input:
                st.error("Ce n'est pas un lien YouTube valide.")
            else:
                st.session_state["videos"] = None
                if scraper.is_playlist(url_input):
                    with st.spinner("📋 Scraping de la playlist en cours..."):
                        playlist_title, videos = scraper.get_playlist_videos(url_input)
                    if not videos:
                        st.error("❌ Impossible de récupérer la playlist.")
                    else:
                        st.session_state["videos"] = videos
                        st.session_state["playlist_title"] = playlist_title
                        st.session_state["is_playlist"] = True
                else:
                    with st.spinner("🌐 Scraping de la vidéo en cours..."):
                        videos = scraper.get_single_video(url_input)
                    if not videos:
                        st.error("❌ Impossible de lire la vidéo.")
                    else:
                        st.session_state["videos"] = videos
                        st.session_state["playlist_title"] = None
                        st.session_state["is_playlist"] = False

        if st.session_state.get("videos"):
            videos = st.session_state["videos"]
            is_playlist = st.session_state.get("is_playlist", False)
            playlist_title = st.session_state.get("playlist_title", "")

            st.markdown('<hr class="divider">', unsafe_allow_html=True)

            if is_playlist:
                st.markdown(f'<div class="playlist-header">📋 {playlist_title}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="playlist-count">{len(videos)} titres trouvés</div>', unsafe_allow_html=True)

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅ Tout sélectionner"):
                        for i in range(len(videos)):
                            st.session_state[f"check_{i}"] = True
                with col_b:
                    if st.button("⬜ Tout désélectionner"):
                        for i in range(len(videos)):
                            st.session_state[f"check_{i}"] = False

                checks = []
                for i, video in enumerate(videos):
                    checked = st.checkbox(
                        f"{video['raw_title']}",
                        value=st.session_state.get(f"check_{i}", True),
                        key=f"check_{i}"
                    )
                    checks.append(checked)

                st.markdown(f'<div style="color:{text3}; font-size:0.8rem; margin-top:0.5rem;">{sum(checks)} titre(s) sélectionné(s)</div>', unsafe_allow_html=True)

            else:
                video = videos[0]
                col_thumb, col_info = st.columns([1, 3])
                if video.get("thumbnail"):
                    with col_thumb:
                        st.image(video["thumbnail"], use_container_width=True)
                with col_info:
                    st.markdown(f'<div style="color:{text3}; font-size:0.75rem;">VIDÉO TROUVÉE</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="font-family:Syne,sans-serif; font-size:1rem; color:{text}; font-weight:700;">{video["raw_title"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="color:{text3}; font-size:0.8rem;">Recherche Spotify : <em>{video["title"]}</em></div>', unsafe_allow_html=True)
                checks = [True]

            st.markdown('<hr class="divider">', unsafe_allow_html=True)

            if st.button("🎵 Ajouter à mes titres likés Spotify"):
                selected_videos = [v for v, c in zip(videos, checks) if c]
                if not selected_videos:
                    st.warning("Sélectionne au moins un titre !")
                else:
                    spotify = SpotifyManager(st.session_state["client_id"], st.session_state["client_secret"])
                    success_count = fail_count = not_found_count = 0
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    for i, video in enumerate(selected_videos):
                        status_text.markdown(f'<div style="color:{text3}; font-size:0.85rem;">🔎 {video["title"]}</div>', unsafe_allow_html=True)
                        track = spotify.search_track(video["title"])
                        if not track:
                            not_found_count += 1
                        else:
                            try:
                                spotify.add_to_favorites(track["uri"])
                                success_count += 1
                            except:
                                fail_count += 1
                        progress_bar.progress((i + 1) / len(selected_videos))

                    status_text.empty()
                    progress_bar.empty()
                    st.markdown('<hr class="divider">', unsafe_allow_html=True)

                    if success_count > 0:
                        st.markdown(
                            f'<div style="background:{success_bg}; border:1px solid #1DB954; border-radius:12px; padding:1rem 1.5rem;">'
                            f'<div style="color:#1DB954; font-family:Syne,sans-serif; font-weight:700;">✅ {success_count} titre(s) ajouté(s) à tes titres likés !</div>'
                            + (f'<div style="color:{text3}; font-size:0.8rem; margin-top:0.3rem;">⚠️ {not_found_count} introuvable(s) sur Spotify</div>' if not_found_count else '')
                            + (f'<div style="color:#ff4444; font-size:0.8rem;">❌ {fail_count} erreur(s)</div>' if fail_count else '')
                            + '</div>', unsafe_allow_html=True
                        )
                    else:
                        st.error("❌ Aucun titre n'a pu être ajouté.")


# ==========================================
# PAGE : COMMENT UTILISER
# ==========================================
elif st.session_state["page"] == "guide":

    st.markdown('<div class="page-title">📖 Comment utiliser</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">Suis ces étapes pour configurer et utiliser le convertisseur</div>', unsafe_allow_html=True)

    # Avertissement prérequis
    st.markdown(f"""
    <div class="warn-box">
        ⚠️ <strong>Prérequis indispensables</strong><br>
        • Un compte <strong>Spotify Premium</strong> est requis pour ajouter des titres via l'API.<br>
        • Un compte <strong>Google/YouTube</strong> pour accéder aux playlists.<br>
        • <strong>Google Chrome</strong> installé sur ton ordinateur (utilisé par le scraper).
    </div>
    """, unsafe_allow_html=True)

    # Section 1 : Créer l'app Spotify
    st.markdown(f'<div style="font-family:Syne,sans-serif; font-weight:700; color:{text}; font-size:1.05rem; margin-bottom:0.8rem;">🎧 Étape 1 — Créer une app Spotify Developer</div>', unsafe_allow_html=True)

    steps_spotify = [
        ("1", "Créer un compte Spotify Developer", f'Va sur <code>developer.spotify.com</code> et connecte-toi avec ton compte Spotify Premium.'),
        ("2", "Créer une nouvelle app", 'Clique sur <b>Create App</b>. Donne-lui un nom (ex: "YT Converter"), une description, et coche uniquement <b>Web API</b>.'),
        ("3", "Configurer le Redirect URI", 'Dans les Settings de ton app, ajoute ce Redirect URI exact : <code>http://127.0.0.1:8888/callback</code> puis clique Save.'),
        ("4", "Ajouter ton compte à l\'allowlist", 'Va dans <b>User Management</b> et ajoute ton adresse email Spotify. Sans ça, l\'API refusera tes requêtes (erreur 403).'),
        ("5", "Récupérer tes clés", 'Dans les Settings, copie le <b>Client ID</b> et le <b>Client Secret</b>. Tu en auras besoin dans le convertisseur.'),
    ]

    for num, title, desc in steps_spotify:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">{num}</div>
            <div class="step-content">
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Section 2 : Utiliser le convertisseur
    st.markdown(f'<div style="font-family:Syne,sans-serif; font-weight:700; color:{text}; font-size:1.05rem; margin-bottom:0.8rem;">🎵 Étape 2 — Utiliser le convertisseur</div>', unsafe_allow_html=True)

    steps_app = [
        ("1", "Connecter Spotify", "Dans la section <b>⚙️ Configuration Spotify</b> du convertisseur, entre ton Client ID et Client Secret puis clique sur Connecter. Une page d'autorisation Spotify s'ouvrira dans ton navigateur."),
        ("2", "Coller un lien YouTube", "Colle l'URL d'une <b>vidéo YouTube</b> (<code>youtube.com/watch?v=...</code>) ou d'une <b>playlist complète</b> (<code>youtube.com/playlist?list=...</code>)."),
        ("3", "Analyser le lien", "Clique sur <b>🔍 Analyser le lien</b>. Le scraper va extraire automatiquement le(s) titre(s) de la page YouTube en arrière-plan."),
        ("4", "Sélectionner les titres", "Pour une playlist, tu verras tous les titres avec des cases à cocher. Sélectionne ceux que tu veux ajouter. Tu peux tout sélectionner ou tout désélectionner d'un coup."),
        ("5", "Ajouter à Spotify", "Clique sur <b>🎵 Ajouter à mes titres likés</b>. Une barre de progression s'affiche pendant l'ajout. Un résumé final te montre combien de titres ont été ajoutés."),
    ]

    for num, title, desc in steps_app:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">{num}</div>
            <div class="step-content">
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # FAQ
    st.markdown(f'<div style="font-family:Syne,sans-serif; font-weight:700; color:{text}; font-size:1.05rem; margin-bottom:0.8rem;">❓ Questions fréquentes</div>', unsafe_allow_html=True)

    faqs = [
        ("Pourquoi j'ai une erreur 403 ?", "L'erreur 403 signifie que Spotify a refusé la requête. Vérifie que : (1) ton compte est bien ajouté dans User Management sur le dashboard, (2) tu as un compte Premium, (3) le Redirect URI est exactement <code>http://127.0.0.1:8888/callback</code>."),
        ("Le titre ajouté sur Spotify n'est pas le bon ?", "Le scraper extrait le titre brut de YouTube et le nettoie, mais parfois le titre YouTube est mal formaté (ex: 'Artist - Song (Remix) [HD]'). Spotify cherche ensuite le titre le plus proche dans sa base. Tu peux modifier manuellement le titre avant d'ajouter."),
        ("Est-ce que ça marche avec les playlists privées YouTube ?", "Non, le scraper ne peut pas accéder aux playlists privées ou non listées. La playlist doit être publique."),
        ("Pourquoi Chrome s'ouvre-t-il en arrière-plan ?", "Le scraper utilise Selenium en mode headless (invisible) pour ouvrir YouTube, accepter les cookies et extraire les titres. Tu ne vois rien car Chrome tourne en arrière-plan."),
    ]

    for question, answer in faqs:
        with st.expander(f"❓ {question}"):
            st.markdown(f'<p style="color:{text2}; font-size:0.87rem; line-height:1.6;">{answer}</p>', unsafe_allow_html=True)


# ==========================================
# PAGE : À PROPOS
# ==========================================
elif st.session_state["page"] == "about":

    st.markdown('<div class="page-title">👥 À propos</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">Le projet et ses créateurs</div>', unsafe_allow_html=True)

    # Description du projet
    st.markdown(f"""
    <div class="info-box">
        🎵 <strong>YT → Spotify</strong> est un convertisseur web qui permet d'extraire les titres
        de vidéos ou playlists YouTube via du <strong>web scraping</strong> (Selenium) et de les ajouter
        automatiquement à tes titres likés Spotify via l'API officielle.<br><br>
        Projet réalisé dans le cadre d'un cours de <strong>scraping Python</strong>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Créateurs
    st.markdown(f'<div style="font-family:Syne,sans-serif; font-weight:700; color:{text}; font-size:1.05rem; margin-bottom:1rem;">🧑‍💻 Créateurs</div>', unsafe_allow_html=True)

    creators = [
        {
            "name": "DIB Adel",
            "role": "Développeur principal",
            "github": "https://github.com/adeldib",
            "initials": "AD"
        },
        {
            "name": "YENER Dogukan",
            "role": "Développeur",
            "github": None,
            "initials": "YD"
        },
        {
            "name": "AIT AMROUCHE Sofiene",
            "role": "Développeur",
            "github": None,
            "initials": "AS"
        },
    ]

    for creator in creators:
        github_btn = f'<a href="{creator["github"]}" target="_blank" style="display:inline-block; margin-top:0.5rem; background:rgba(29,185,84,0.12); color:#1DB954; border:1px solid rgba(29,185,84,0.3); border-radius:20px; padding:0.25rem 0.8rem; font-size:0.78rem; text-decoration:none; font-family:DM Sans,sans-serif;">GitHub →</a>' if creator["github"] else ''

        st.markdown(f"""
        <div class="step-card" style="align-items:center;">
            <div style="background:linear-gradient(135deg,#1DB954,#17a349); color:#000; font-family:Syne,sans-serif; font-weight:800; font-size:0.85rem; width:42px; height:42px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0; letter-spacing:-0.5px;">
                {creator["initials"]}
            </div>
            <div>
                <div style="font-family:Syne,sans-serif; font-weight:700; color:{text}; font-size:0.95rem;">{creator["name"]}</div>
                <div style="color:{text3}; font-size:0.8rem;">{creator["role"]}</div>
                {github_btn}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Stack technique
    st.markdown(f'<div style="font-family:Syne,sans-serif; font-weight:700; color:{text}; font-size:1.05rem; margin-bottom:0.8rem;">🛠️ Stack technique</div>', unsafe_allow_html=True)

    techs = [
        ("🐍 Python", "Langage principal"),
        ("⚡ Streamlit", "Interface web"),
        ("🌐 Selenium", "Web scraping YouTube"),
        ("🎵 Spotipy", "API Spotify"),
        ("🔍 Regex", "Nettoyage des titres"),
    ]

    cols = st.columns(2)
    for i, (tech, desc) in enumerate(techs):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background:{step_bg}; border:1px solid {step_border}; border-radius:10px; padding:0.7rem 1rem; margin-bottom:0.6rem;">
                <div style="font-family:Syne,sans-serif; font-weight:700; color:{text}; font-size:0.88rem;">{tech}</div>
                <div style="color:{text3}; font-size:0.78rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)