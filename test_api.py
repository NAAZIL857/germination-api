# -*- coding: utf-8 -*-
"""Script de test pour l'API"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Test de l'API de Prédiction de Germination\n")
    
    # Test 1: Page d'accueil
    print("1️⃣ Test de la page d'accueil...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")
    
    # Test 2: Prédiction pour le maïs
    print("2️⃣ Test de prédiction pour le maïs...")
    data_mais = {
        "seed_type": "mais",
        "temperature": 25,
        "soil_humidity": 70,
        "light_level": 8,
        "pH_du_sol": 6.2
    }
    response = requests.post(f"{BASE_URL}/predict", json=data_mais)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")
    
    # Test 3: Prédiction pour le riz
    print("3️⃣ Test de prédiction pour le riz...")
    data_riz = {
        "seed_type": "riz",
        "temperature": 28,
        "soil_humidity": 80,
        "light_level": 7,
        "pH_du_sol": 6.0
    }
    response = requests.post(f"{BASE_URL}/predict", json=data_riz)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")
    
    # Test 4: Conditions optimales
    print("4️⃣ Test des conditions optimales...")
    response = requests.get(f"{BASE_URL}/conditions/mais")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")
    
    # Test 5: Ajouter des données de capteurs
    print("5️⃣ Test d'ajout de données de capteurs...")
    sensor_data = {
        "seed_type": "mais",
        "temperature": 22,
        "soil_humidity": 65,
        "light_level": 7,
        "pH_du_sol": 5.8,
        "germination_score": 90
    }
    response = requests.post(f"{BASE_URL}/sensor-data", json=sensor_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")
    
    # Test 6: Récupérer l'historique des prédictions
    print("6️⃣ Test de récupération de l'historique...")
    response = requests.get(f"{BASE_URL}/predictions?limit=5")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Nombre de prédictions: {result['count']}\n")
    
    # Test 7: Statistiques
    print("7️⃣ Test des statistiques...")
    response = requests.get(f"{BASE_URL}/stats/mais")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")
    
    # Test 8: Health check
    print("8️⃣ Test du health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")
    
    print("✅ Tous les tests sont terminés!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: L'API n'est pas accessible. Assurez-vous qu'elle est démarrée avec: python api.py")
    except Exception as e:
        print(f"❌ Erreur: {e}")
