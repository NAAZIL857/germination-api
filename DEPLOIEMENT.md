# Guide de Déploiement de l'API 🚀

Ce guide vous explique comment mettre votre API en ligne gratuitement.

## 🌐 Options de Déploiement Gratuites

### Option 1: Render (Recommandé) ⭐

**Avantages:**
- Gratuit
- Facile à utiliser
- Déploiement automatique depuis GitHub
- HTTPS inclus
- Pas de limite de temps

**Étapes:**

1. **Créer un compte sur Render**
   - Allez sur https://render.com
   - Inscrivez-vous gratuitement

2. **Créer un dépôt GitHub**
   - Allez sur https://github.com
   - Créez un nouveau repository (ex: germination-api)
   - Uploadez tous les fichiers du projet

3. **Déployer sur Render**
   - Sur Render, cliquez "New +" → "Web Service"
   - Connectez votre repository GitHub
   - Configurez:
     - Name: germination-api
     - Environment: Python 3
     - Build Command: `pip install -r requirements_deploy.txt`
     - Start Command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
   - Cliquez "Create Web Service"

4. **Votre API sera accessible à:**
   ```
   https://germination-api.onrender.com
   ```

---

### Option 2: Railway

**Avantages:**
- Gratuit (500h/mois)
- Très simple
- Déploiement rapide

**Étapes:**

1. **Créer un compte sur Railway**
   - Allez sur https://railway.app
   - Inscrivez-vous avec GitHub

2. **Déployer**
   - Cliquez "New Project"
   - Sélectionnez "Deploy from GitHub repo"
   - Choisissez votre repository
   - Railway détecte automatiquement Python

3. **Configurer**
   - Ajoutez la variable d'environnement: `PORT=8000`
   - Railway génère une URL automatiquement

---

### Option 3: PythonAnywhere

**Avantages:**
- Gratuit
- Spécialisé Python
- Pas besoin de GitHub

**Étapes:**

1. **Créer un compte**
   - Allez sur https://www.pythonanywhere.com
   - Créez un compte gratuit

2. **Uploader les fichiers**
   - Dans "Files", uploadez tous vos fichiers
   - Ou utilisez Git pour cloner votre repo

3. **Configurer l'application web**
   - Allez dans "Web"
   - Créez une nouvelle application WSGI
   - Configurez le fichier WSGI pour pointer vers votre API

---

### Option 4: Ngrok (Test rapide)

**Pour tester rapidement sans déploiement permanent:**

1. **Installer ngrok**
   ```bash
   # Téléchargez depuis https://ngrok.com
   ```

2. **Démarrer votre API localement**
   ```bash
   python api.py
   ```

3. **Exposer avec ngrok**
   ```bash
   ngrok http 8000
   ```

4. **Vous obtenez une URL publique:**
   ```
   https://xxxx-xx-xx-xxx-xxx.ngrok.io
   ```

---

## 📝 Préparation avant le déploiement

### 1. Créer un repository GitHub

```bash
# Dans le dossier du projet
git init
git add .
git commit -m "Initial commit - API Germination"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/germination-api.git
git push -u origin main
```

### 2. Vérifier les fichiers nécessaires

✅ Fichiers créés pour le déploiement:
- `requirements_deploy.txt` - Dépendances
- `Procfile` - Configuration Heroku
- `runtime.txt` - Version Python
- `render.yaml` - Configuration Render
- `.gitignore` - Fichiers à ignorer

---

## 🧪 Tester l'API déployée

Une fois déployée, testez avec:

```python
import requests

# Remplacez par votre URL
API_URL = "https://votre-api.onrender.com"

response = requests.post(f"{API_URL}/predict", json={
    "seed_type": "tomate",
    "temperature": 25,
    "soil_humidity": 75,
    "light_level": 11,
    "pH_du_sol": 6.4
})

print(response.json())
```

Ou dans le navigateur:
```
https://votre-api.onrender.com/docs
```

---

## 🔧 Configuration CORS

L'API est déjà configurée pour accepter les requêtes de n'importe quel domaine.

Si vous voulez restreindre:

```python
# Dans api.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://votre-site.com"],  # Domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Surveillance

### Render
- Logs en temps réel dans le dashboard
- Métriques de performance

### Railway
- Logs dans l'interface
- Monitoring automatique

---

## 💰 Limites des plans gratuits

| Service | Limite | Uptime |
|---------|--------|--------|
| Render | 750h/mois | Dort après 15min inactivité |
| Railway | 500h/mois | Toujours actif |
| PythonAnywhere | Toujours actif | Limité en CPU |
| Ngrok | Session temporaire | Tant que connecté |

---

## 🚀 Déploiement Recommandé: Render

**Pourquoi Render?**
- ✅ Gratuit et illimité
- ✅ HTTPS automatique
- ✅ Déploiement automatique depuis GitHub
- ✅ Facile à configurer
- ✅ Logs et monitoring inclus

**Commencez maintenant:**
1. Créez un compte sur https://render.com
2. Connectez votre GitHub
3. Déployez en 2 clics!

---

## 📞 Support

Pour toute question sur le déploiement:
- Documentation Render: https://render.com/docs
- Documentation Railway: https://docs.railway.app
- Documentation PythonAnywhere: https://help.pythonanywhere.com

---

## 🔗 Exemple d'URL finale

Après déploiement, votre API sera accessible à:
```
https://germination-api.onrender.com
https://germination-api.onrender.com/docs
https://germination-api.onrender.com/predict
```

Vous pourrez l'appeler depuis n'importe où:
- Applications web
- Applications mobiles
- Scripts Python
- Arduino/ESP32
- Postman
