# -*- coding: utf-8 -*-
"""Test simple et rapide de l'API"""
import requests
import json

print("="*60)
print("  TEST SIMPLE DE L'API")
print("="*60)

# Test 1: Prédiction pour le maïs
print("\n1. Prediction pour le mais:")
print("-"*60)

data = {
    "seed_type": "mais",
    "temperature": 25,
    "soil_humidity": 70,
    "light_level": 8,
    "pH_du_sol": 6.2
}

response = requests.post("http://localhost:8000/predict", json=data)
result = response.json()

print(f"Score predit: {result['predicted_score']}")
print(f"\nRecommandations:")
for rec in result['recommendations']:
    print(f"  - {rec}")

# Test 2: Prédiction pour le riz avec mauvaises conditions
print("\n\n2. Prediction pour le riz (mauvaises conditions):")
print("-"*60)

data2 = {
    "seed_type": "riz",
    "temperature": 15,
    "soil_humidity": 50,
    "light_level": 3,
    "pH_du_sol": 4.5
}

response2 = requests.post("http://localhost:8000/predict", json=data2)
result2 = response2.json()

print(f"Score predit: {result2['predicted_score']}")
print(f"\nRecommandations:")
for rec in result2['recommendations']:
    print(f"  - {rec}")

# Test 3: Conditions optimales
print("\n\n3. Conditions optimales pour le mais:")
print("-"*60)

response3 = requests.get("http://localhost:8000/conditions/mais")
result3 = response3.json()

print(json.dumps(result3, indent=2, ensure_ascii=False))

print("\n" + "="*60)
print("  TESTS TERMINES AVEC SUCCES!")
print("="*60)
print("\nVous pouvez maintenant:")
print("  - Tester dans le navigateur: http://localhost:8000/docs")
print("  - Integrer l'API dans votre systeme")
print("="*60)
