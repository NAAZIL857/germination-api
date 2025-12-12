# API de Prédiction de Germination 🌱

API REST pour prédire les scores de germination des graines et obtenir des recommandations basées sur les conditions environnementales.

## 🚀 Installation

```bash
pip install -r requirements.txt
```

## 📦 Démarrage de l'API

```bash
python api.py
```

L'API sera accessible sur: `http://localhost:8000`

Documentation interactive: `http://localhost:8000/docs`

## 📊 Base de Données

La base de données SQLite (`germination.db`) stocke:
- **sensor_data**: Données des capteurs avec scores de germination réels
- **predictions**: Historique des prédictions effectuées

## 🔌 Endpoints Disponibles

### 1. Page d'accueil
```
GET /
```
Retourne les informations sur l'API et la liste des endpoints.

 ### 2. Prédiction complète
```
POST /predict
```
**Body:**
```json
{
  "seed_type": "tomate",
  "temperature": 25,
  "soil_humidity": 75,
  "air_humidity": 70,
  "light_level": 11
}
```

Types supportés: mais, riz, ble, soja, tomate, haricot, carotte, laitue, concombre, poivron
**Response:**
```json
{
  "predicted_score": 95.23,
  "recommendations": ["✅ Conditions optimales pour le mais."],
  "seed_type": "mais",
  "conditions": {...}
}
```

### 3. Recommandations uniquement
```
POST /recommendations
```
Même format que `/predict` mais retourne uniquement les recommandations.

### 4. Conditions optimales
```
GET /conditions/{seed_type}
GET /conditions
```
Retourne les conditions optimales pour un type de graine ou tous les types.

### 5. Ajouter des données de capteurs
```
POST /sensor-data
```
**Body:**
```json
{
  "seed_type": "mais",
  "temperature": 22,
  "soil_humidity": 65,
  "air_humidity": 60,
  "light_level": 7,
  "germination_score": 90
}
```

### 6. Récupérer les données de capteurs
```
GET /sensor-data?limit=100
```

### 7. Historique des prédictions
```
GET /predictions?limit=100
```

### 8. Statistiques par type de graine
```
GET /stats/{seed_type}
```
Retourne: count, avg_score, min_score, max_score

### 9. Health Check
```
GET /health
```

## 🧪 Tester l'API

### Avec le script de test:
```bash
python test_api.py
```

### Avec curl:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"seed_type":"mais","temperature":25,"soil_humidity":70,"air_humidity":60,"light_level":8}'
```

### Avec Python:
```python
import requests

# Exemple avec tomate
response = requests.post("http://localhost:8000/predict", json={
    "seed_type": "tomate",
    "temperature": 25,
    "soil_humidity": 75,
    "air_humidity": 70,
    "light_level": 11
})

print(response.json())

# Exemple avec laitue
response = requests.post("http://localhost:8000/predict", json={
    "seed_type": "laitue",
    "temperature": 15,
    "soil_humidity": 70,
    "air_humidity": 60,
    "light_level": 6
})

print(response.json())
```

## 📝 Types de Graines Supportés (10)

- **mais**: Maïs (18-30°C, sol 60-80%, air 50-70%, 6-10h lumière)
- **riz**: Riz (20-35°C, sol 70-90%, air 60-80%, 5-9h lumière)
- **ble**: Blé (15-25°C, sol 50-70%, air 40-60%, 6-10h lumière)
- **soja**: Soja (20-30°C, sol 60-75%, air 50-70%, 7-12h lumière)
- **tomate**: Tomate (20-30°C, sol 65-85%, air 60-80%, 8-14h lumière)
- **haricot**: Haricot (18-28°C, sol 60-80%, air 50-70%, 6-10h lumière)
- **carotte**: Carotte (15-25°C, sol 55-75%, air 45-65%, 5-8h lumière)
- **laitue**: Laitue (10-20°C, sol 60-80%, air 50-70%, 4-8h lumière)
- **concombre**: Concombre (20-30°C, sol 70-90%, air 60-80%, 8-12h lumière)
- **poivron**: Poivron (22-30°C, sol 65-85%, air 60-80%, 8-14h lumière)

## 🔧 Configuration

L'API utilise:
- **Port**: 8000 (modifiable dans `api.py`)
- **Host**: 0.0.0.0 (accessible depuis le réseau)
- **Base de données**: SQLite (`germination.db`)
- **Modèle**: Entraîné au démarrage depuis `sensors_data.csv`

## 📈 Intégration avec d'autres systèmes

L'API peut être facilement intégrée avec:
- Applications web (React, Vue, Angular)
- Applications mobiles (React Native, Flutter)
- Systèmes IoT (capteurs Arduino, Raspberry Pi)
- Dashboards de monitoring
- Systèmes d'automatisation agricole

## 🛡️ Validation des Données

L'API valide automatiquement:
- `temperature`: -10°C à 50°C
- `soil_humidity`: 0% à 100%
- `air_humidity`: 0% à 100%
- `light_level`: 0h à 24h

## 📊 Paramètres des Capteurs

- **temperature**: Température ambiante en °C
- **soil_humidity**: Humidité du sol en %
- **air_humidity**: Humidité de l'air en %
- **light_level**: Heures d'exposition à la lumière par jour
