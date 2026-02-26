# 1. Image de base Python légère
FROM python:3.9-slim

# 2. Désactiver les questions interactives pendant l'installation
ENV DEBIAN_FRONTEND=noninteractive

# 3. Installer Chromium (la version open-source de Chrome) et son driver pour Selenium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# 4. Définir le dossier de travail
WORKDIR /app

# 5. Copier uniquement les requirements en premier (optimisation du cache Docker)
COPY requirements.txt .

# 6. Installer les librairies Python (Streamlit, Selenium, Spotipy...)
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copier tout le reste du code de ton projet
COPY . .

# 8. Récupérer le port dynamique de Railway (ou 8080 par défaut)
ENV PORT=8080
EXPOSE $PORT

# 9. La commande pour lancer ton interface Streamlit
CMD sh -c "streamlit run projet.py --server.port=$PORT --server.address=0.0.0.0"