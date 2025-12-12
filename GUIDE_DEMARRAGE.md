# 🚀 Guide de Démarrage Rapide

## 📋 Vue d'ensemble du projet

Ce projet fournit une **API REST** pour prédire les scores de germination des graines (maïs et riz) basée sur les conditions environnementales.

### 🗂️ Structure du projet

```
seed_germination_ai/
├── main.py              # Modèle IA et logique de prédiction
├── database.py          # Gestion de la base de données SQLite
├── api.py               # API REST avec FastAPI
├── sensors_data.csv     # Données d'entraînement
├── requirements.txt     # Dépendances Python
├── start_api.bat        # Script de démarrage Windows
├── test_api.py          # Tests automatisés de l'API
├── example_client.py    # Exemple d'utilisation de l'API
└── README_API.md        # Documentation complète de l'API
```

## ⚡ Démarrage en 3 étapes

### 1️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2️⃣ Démarrer l'API

**Option A - Avec le script batch (Windows):**
```bash
start_api.bat
```

**Option B - Avec Python:**
```bash
python api.py
```

### 3️⃣ Accéder à l'API

- **API**: http://localhost:8000
- **Documentation interactive**: http://localhost:8000/docs
- **Documentation alternative**: http://localhost:8000/redoc

## 🧪 Tester l'API

### Test automatique complet
```bash
python test_api.py
```

### Test avec l'exemple de client
```bash
python example_client.py
```

### Test manuel avec curl
```bash
curl -X POST "http://localhost:8000/predict" ^
  -H "Content-Type: application/json" ^
  -d "{\"seed_type\":\"mais\",\"temperature\":25,\"soil_humidity\":70,\"light_level\":8,\"pH_du_sol\":6.2}"
```

## 📊 Base de données

La base de données `germination.db` est créée automatiquement au premier démarrage.

**Tables:**
- `sensor_data`: Données des capteurs avec scores réels
- `predictions`: Historique des prédictions

## 🔌 Endpoints principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Informations sur l'API |
| POST | `/predict` | Prédiction + recommandations |
| POST | `/recommendations` | Recommandations uniquement |
| GET | `/conditions/{seed_type}` | Conditions optimales |
| POST | `/sensor-data` | Ajouter des données |
| GET | `/predictions` | Historique |
| GET | `/stats/{seed_type}` | Statistiques |
| GET | `/health` | État de l'API |

## 💡 Exemples d'utilisation

### Python
```python
import requests

# Prédiction
response = requests.post("http://localhost:8000/predict", json={
    "seed_type": "mais",
    "temperature": 25,
    "soil_humidity": 70,
    "light_level": 8,
    "pH_du_sol": 6.2
})

result = response.json()
print(f"Score: {result['predicted_score']}")
print(f"Recommandations: {result['recommendations']}")
```

### JavaScript (fetch)
```javascript
fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    seed_type: 'mais',
    temperature: 25,
    soil_humidity: 70,
    light_level: 8,
    pH_du_sol: 6.2
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

### Arduino/ESP32 (C++)
```cpp
#include <HTTPClient.h>
#include <ArduinoJson.h>

HTTPClient http;
http.begin("http://192.168.1.100:8000/predict");
http.addHeader("Content-Type", "application/json");

StaticJsonDocument<200> doc;
doc["seed_type"] = "mais";
doc["temperature"] = 25.5;
doc["soil_humidity"] = 70.0;
doc["light_level"] = 8.0;
doc["pH_du_sol"] = 6.2;

String json;
serializeJson(doc, json);
int httpCode = http.POST(json);

if (httpCode == 200) {
  String response = http.getString();
  Serial.println(response);
}
```

## 🔧 Configuration

### Changer le port
Dans `api.py`, ligne finale:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Modifier le port ici
```

### Accès réseau
L'API est accessible depuis d'autres machines sur le réseau local via:
```
http://[VOTRE_IP]:8000
```

Pour trouver votre IP:
```bash
ipconfig  # Windows
```

## 📱 Intégration avec d'autres systèmes

L'API peut être intégrée avec:
- ✅ Applications web (React, Vue, Angular)
- ✅ Applications mobiles (React Native, Flutter)
- ✅ Systèmes IoT (Arduino, Raspberry Pi, ESP32)
- ✅ Dashboards (Grafana, Tableau)
- ✅ Automatisation (Node-RED, Home Assistant)

## 🛠️ Développement

### Ajouter un nouveau type de graine

1. Dans `main.py`, ajouter dans `OPTIMAL_CONDITIONS`:
```python
'ble': {
    'temperature': (15, 25),
    'soil_humidity': (50, 70),
    'light_level': (6, 10),
    'pH_du_sol': (6.0, 7.5)
}
```

2. Ajouter des données dans `sensors_data.csv`

3. Redémarrer l'API

### Personnaliser les recommandations

Modifier les dictionnaires dans `main.py`:
- `OPTIMAL_CONDITIONS`
- `RECOMMENDATIONS_PH`

## 📚 Documentation complète

Consultez `README_API.md` pour la documentation détaillée de tous les endpoints.

## ❓ Dépannage

**L'API ne démarre pas:**
- Vérifier que le port 8000 n'est pas déjà utilisé
- Vérifier que toutes les dépendances sont installées

**Erreur de connexion:**
- Vérifier que l'API est démarrée
- Vérifier l'URL (http://localhost:8000)

**Erreur de prédiction:**
- Vérifier que `sensors_data.csv` existe
- Vérifier le format des données d'entrée

## 📞 Support

Pour toute question, consultez:
- Documentation interactive: http://localhost:8000/docs
- Fichier README_API.md
- Code d'exemple: example_client.py
