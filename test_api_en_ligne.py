# -*- coding: utf-8 -*-
"""
Script pour tester l'API une fois déployée en ligne
"""
import requests
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# REMPLACEZ PAR VOTRE URL DEPLOYEE
API_URL = input("Entrez l'URL de votre API (ex: https://votre-api.onrender.com): ").strip()

if not API_URL:
    API_URL = "http://localhost:8000"
    print(f"Utilisation de l'URL locale: {API_URL}")

print("\n" + "="*70)
print(f"  TEST DE L'API EN LIGNE")
print(f"  URL: {API_URL}")
print("="*70)

# Test 1: Health check
print("\n1. Test de connexion (health check)...")
try:
    response = requests.get(f"{API_URL}/health", timeout=10)
    if response.status_code == 200:
        print("   ✓ API accessible!")
        print(f"   Status: {response.json()}")
    else:
        print(f"   ✗ Erreur: Status {response.status_code}")
except Exception as e:
    print(f"   ✗ Impossible de se connecter: {e}")
    sys.exit(1)

# Test 2: Page d'accueil
print("\n2. Test de la page d'accueil...")
try:
    response = requests.get(f"{API_URL}/", timeout=10)
    data = response.json()
    print(f"   Version: {data.get('version')}")
    print(f"   Semences supportees: {data.get('semences_supportees')}")
except Exception as e:
    print(f"   ✗ Erreur: {e}")

# Test 3: Prédiction tomate
print("\n3. Test de prediction (tomate)...")
try:
    response = requests.post(f"{API_URL}/predict", json={
        "seed_type": "tomate",
        "temperature": 25,
        "soil_humidity": 75,
        "light_level": 11,
        "pH_du_sol": 6.4
    }, timeout=10)
    
    result = response.json()
    print(f"   Score predit: {result['predicted_score']}")
    print(f"   Recommandation: {result['recommendations'][0][:60]}...")
except Exception as e:
    print(f"   ✗ Erreur: {e}")

# Test 4: Conditions optimales
print("\n4. Test des conditions optimales...")
try:
    response = requests.get(f"{API_URL}/conditions", timeout=10)
    conditions = response.json()
    print(f"   Nombre de semences: {len(conditions['conditions'])}")
    print(f"   Types: {', '.join(list(conditions['conditions'].keys())[:5])}...")
except Exception as e:
    print(f"   ✗ Erreur: {e}")

print("\n" + "="*70)
print("  TESTS TERMINES!")
print("="*70)
print(f"\nVotre API est accessible a: {API_URL}")
print(f"Documentation: {API_URL}/docs")
print("\nVous pouvez maintenant l'utiliser depuis n'importe ou!")
print("="*70)
