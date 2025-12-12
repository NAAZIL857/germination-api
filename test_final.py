# -*- coding: utf-8 -*-
import requests
import json
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("="*60)
print("  TEST DE L'API")
print("="*60)

print("\n1. Test prediction pour le mais:")
data = {
    "seed_type": "mais",
    "temperature": 25,
    "soil_humidity": 70,
    "light_level": 8,
    "pH_du_sol": 6.2
}

response = requests.post("http://localhost:8000/predict", json=data)
result = response.json()

print(f"Score: {result['predicted_score']}")
print("Recommandations:")
for rec in result['recommendations']:
    print(f"  - {rec}")

print("\n2. Test prediction pour le riz (mauvaises conditions):")
data2 = {
    "seed_type": "riz",
    "temperature": 15,
    "soil_humidity": 50,
    "light_level": 3,
    "pH_du_sol": 4.5
}

response2 = requests.post("http://localhost:8000/predict", json=data2)
result2 = response2.json()

print(f"Score: {result2['predicted_score']}")
print("Recommandations:")
for rec in result2['recommendations']:
    print(f"  - {rec}")

print("\n" + "="*60)
print("TESTS TERMINES!")
print("="*60)
