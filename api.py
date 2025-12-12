# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
import os
from main import train_germination_model, get_recommendations, predict_score, OPTIMAL_CONDITIONS
from database import GerminationDatabase

# Initialisation
app = FastAPI(
    title="API de Prédiction de Germination",
    description="API pour prédire les scores de germination et obtenir des recommandations pour 10 types de semences",
    version="2.0.0"
)

# Configuration CORS pour permettre les appels depuis n'importe quel domaine
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = GerminationDatabase()

# Entraîner le modèle au démarrage
model, model_columns = train_germination_model('sensors_data.csv')

# --- Modèles Pydantic ---
class SensorInput(BaseModel):
    seed_type: str = Field(..., description="Type de graine (mais, riz, ble, etc.)")
    temperature: float = Field(..., ge=-10, le=50, description="Température en °C")
    soil_humidity: float = Field(..., ge=0, le=100, description="Humidité du sol en %")
    air_humidity: float = Field(..., ge=0, le=100, description="Humidité de l'air en %")
    light_level: float = Field(..., ge=0, le=100, description="Niveau de luminosité en % (0-100)")

    class Config:
        json_schema_extra = {
            "example": {
                "seed_type": "tomate",
                "temperature": 25,
                "soil_humidity": 75,
                "air_humidity": 70,
                "light_level": 65
            }
        }

class PredictionResponse(BaseModel):
    predicted_score: float
    recommendations: List[str]
    seed_type: str
    conditions: dict

class SensorDataInput(BaseModel):
    seed_type: str
    temperature: float
    soil_humidity: float
    air_humidity: float
    light_level: float
    germination_score: Optional[float] = None

# --- Endpoints ---
@app.get("/")
def root():
    """Page d'accueil de l'API"""
    return {
        "message": "API de Prédiction de Germination",
        "version": "2.0.0",
        "semences_supportees": 10,
        "types_semences": ["mais", "riz", "ble", "soja", "tomate", "haricot", "carotte", "laitue", "concombre", "poivron"],
        "endpoints": {
            "POST /predict": "Prédire le score de germination",
            "POST /recommendations": "Obtenir des recommandations",
            "GET /conditions/{seed_type}": "Obtenir les conditions optimales",
            "POST /sensor-data": "Ajouter des données de capteurs",
            "GET /sensor-data": "Récupérer les données de capteurs",
            "GET /predictions": "Récupérer l'historique des prédictions",
            "GET /stats/{seed_type}": "Obtenir les statistiques"
        }
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(data: SensorInput):
    """Prédit le score de germination et retourne des recommandations"""
    try:
        # Préparer les données
        input_data = {
            'seed_type': data.seed_type,
            'temperature': data.temperature,
            'soil_humidity': data.soil_humidity,
            'air_humidity': data.air_humidity,
            'light_level': data.light_level
        }
        
        # Prédiction
        score = predict_score(model, model_columns, input_data)
        predicted_score = float(score[0])
        
        # Recommandations
        recommendations = get_recommendations(**input_data)
        
        # Enregistrer dans la base de données
        db.add_prediction(
            data.seed_type, data.temperature, data.soil_humidity,
            data.air_humidity, data.light_level, predicted_score
        )
        
        return {
            "predicted_score": round(predicted_score, 2),
            "recommendations": recommendations,
            "seed_type": data.seed_type,
            "conditions": input_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommendations")
def recommendations(data: SensorInput):
    """Retourne uniquement les recommandations sans prédiction"""
    try:
        recs = get_recommendations(
            data.seed_type, data.temperature, data.soil_humidity,
            data.air_humidity, data.light_level
        )
        return {"recommendations": recs, "seed_type": data.seed_type}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conditions/{seed_type}")
def get_conditions(seed_type: str):
    """Retourne les conditions optimales pour un type de graine"""
    if seed_type not in OPTIMAL_CONDITIONS:
        raise HTTPException(status_code=404, detail=f"Type de graine '{seed_type}' non trouvé")
    
    return {
        "seed_type": seed_type,
        "optimal_conditions": OPTIMAL_CONDITIONS[seed_type]
    }

@app.get("/conditions")
def get_all_conditions():
    """Retourne toutes les conditions optimales"""
    return {"conditions": OPTIMAL_CONDITIONS}

@app.post("/sensor-data")
def add_sensor_data(data: SensorDataInput):
    """Ajoute des données de capteurs dans la base de données"""
    try:
        data_id = db.add_sensor_data(
            data.seed_type, data.temperature, data.soil_humidity,
            data.air_humidity, data.light_level, data.germination_score
        )
        return {"message": "Données ajoutées avec succès", "id": data_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sensor-data")
def get_sensor_data(limit: int = 100):
    """Récupère les données de capteurs"""
    try:
        data = db.get_sensor_data(limit)
        return {"count": len(data), "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predictions")
def get_predictions(limit: int = 100):
    """Récupère l'historique des prédictions"""
    try:
        predictions = db.get_predictions(limit)
        return {"count": len(predictions), "predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats/{seed_type}")
def get_stats(seed_type: str):
    """Récupère les statistiques pour un type de graine"""
    try:
        stats = db.get_stats_by_seed_type(seed_type)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Vérifie l'état de l'API"""
    return {"status": "healthy", "model_loaded": model is not None}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print("="*70)
    print("  API DE PREDICTION DE GERMINATION")
    print("  10 types de semences supportes")
    print("="*70)
    print("\n[OK] Demarrage de l'API...\n")
    print("IMPORTANT: Utilisez ces URLs dans votre navigateur:")
    print(f"  -> http://localhost:{port}")
    print(f"  -> http://127.0.0.1:{port}")
    print(f"\nDocumentation interactive:")
    print(f"  -> http://localhost:{port}/docs")
    print("\nSemences: mais, riz, ble, soja, tomate, haricot,")
    print("          carotte, laitue, concombre, poivron")
    print("\nParametres: temperature, soil_humidity, air_humidity, light_level")
    print("\nAppuyez sur CTRL+C pour arreter")
    print("="*70)
    print("\n")
    uvicorn.run(app, host="0.0.0.0", port=port)
