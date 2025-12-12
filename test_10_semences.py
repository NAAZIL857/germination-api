# -*- coding: utf-8 -*-
import requests
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("="*70)
print("  TEST DES 10 TYPES DE SEMENCES")
print("="*70)

semences = [
    {"seed_type": "mais", "temperature": 25, "soil_humidity": 70, "light_level": 8, "pH_du_sol": 6.2},
    {"seed_type": "riz", "temperature": 28, "soil_humidity": 80, "light_level": 7, "pH_du_sol": 6.0},
    {"seed_type": "ble", "temperature": 20, "soil_humidity": 60, "light_level": 8, "pH_du_sol": 6.5},
    {"seed_type": "soja", "temperature": 25, "soil_humidity": 68, "light_level": 9, "pH_du_sol": 6.5},
    {"seed_type": "tomate", "temperature": 25, "soil_humidity": 75, "light_level": 11, "pH_du_sol": 6.4},
    {"seed_type": "haricot", "temperature": 23, "soil_humidity": 70, "light_level": 8, "pH_du_sol": 6.5},
    {"seed_type": "carotte", "temperature": 20, "soil_humidity": 65, "light_level": 6, "pH_du_sol": 6.2},
    {"seed_type": "laitue", "temperature": 15, "soil_humidity": 70, "light_level": 6, "pH_du_sol": 6.5},
    {"seed_type": "concombre", "temperature": 25, "soil_humidity": 80, "light_level": 10, "pH_du_sol": 6.5},
    {"seed_type": "poivron", "temperature": 26, "soil_humidity": 75, "light_level": 11, "pH_du_sol": 6.4}
]

for i, data in enumerate(semences, 1):
    print(f"\n{i}. {data['seed_type'].upper()}")
    print("-" * 70)
    
    try:
        response = requests.post("http://localhost:8000/predict", json=data)
        result = response.json()
        
        print(f"   Score predit: {result['predicted_score']}")
        print(f"   Recommandations: {result['recommendations'][0][:50]}...")
    except Exception as e:
        print(f"   Erreur: {e}")

print("\n" + "="*70)
print("  TOUTES LES SEMENCES ONT ETE TESTEES!")
print("="*70)

# Test des conditions optimales
print("\n\nCONDITIONS OPTIMALES DISPONIBLES:")
print("="*70)
response = requests.get("http://localhost:8000/conditions")
conditions = response.json()

for seed_type in conditions['conditions'].keys():
    print(f"  - {seed_type}")

print("="*70)
