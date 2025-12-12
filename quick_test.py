# -*- coding: utf-8 -*-
"""Test rapide pour vérifier que tous les modules fonctionnent"""
import sys
import io

# Configurer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("🧪 Test rapide des modules...\n")

# Test 1: Module principal
print("1️⃣ Test du module principal (main.py)...")
try:
    from main import train_germination_model, get_recommendations, predict_score
    model, model_columns = train_germination_model('sensors_data.csv')
    print("   ✅ Module principal OK\n")
except Exception as e:
    print(f"   ❌ Erreur: {e}\n")
    sys.exit(1)

# Test 2: Base de données
print("2️⃣ Test de la base de données (database.py)...")
try:
    from database import GerminationDatabase
    db = GerminationDatabase('test_germination.db')
    test_id = db.add_sensor_data('mais', 25, 70, 8, 6.2, 95)
    print(f"   ✅ Base de données OK (ID test: {test_id})\n")
except Exception as e:
    print(f"   ❌ Erreur: {e}\n")
    sys.exit(1)

# Test 3: Prédiction
print("3️⃣ Test de prédiction...")
try:
    data = {
        'seed_type': 'mais',
        'temperature': 25,
        'soil_humidity': 70,
        'air_humidity': 60,
        'light_level': 8
    }
    score = predict_score(model, model_columns, data)
    recs = get_recommendations(**data)
    print(f"   Score prédit: {score[0]:.2f}")
    print(f"   Recommandations: {len(recs)} trouvées")
    print("   ✅ Prédiction OK\n")
except Exception as e:
    print(f"   ❌ Erreur: {e}\n")
    sys.exit(1)

# Test 4: Vérifier les dépendances de l'API
print("4️⃣ Test des dépendances de l'API...")
try:
    import fastapi
    import uvicorn
    import pydantic
    import requests
    print("   ✅ Toutes les dépendances sont installées\n")
except ImportError as e:
    print(f"   ❌ Dépendance manquante: {e}\n")
    print("   Exécutez: pip install -r requirements.txt\n")
    sys.exit(1)

print("=" * 60)
print("✅ TOUS LES TESTS SONT PASSÉS!")
print("=" * 60)
print("\n🚀 Vous pouvez maintenant démarrer l'API avec:")
print("   python api.py")
print("   OU")
print("   start_api.bat")
print("\n📖 Documentation: http://localhost:8000/docs")
