# -*- coding: utf-8 -*-
"""
Exemple d'utilisation de l'API de prédiction de germination
Ce script montre comment intégrer l'API dans une autre application
"""
import requests
import json

class GerminationClient:
    """Client pour interagir avec l'API de prédiction de germination"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def predict(self, seed_type, temperature, soil_humidity, light_level, pH_du_sol):
        """Obtenir une prédiction et des recommandations"""
        url = f"{self.base_url}/predict"
        data = {
            "seed_type": seed_type,
            "temperature": temperature,
            "soil_humidity": soil_humidity,
            "light_level": light_level,
            "pH_du_sol": pH_du_sol
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête: {e}")
            return None
    
    def get_optimal_conditions(self, seed_type):
        """Obtenir les conditions optimales pour un type de graine"""
        url = f"{self.base_url}/conditions/{seed_type}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête: {e}")
            return None
    
    def get_statistics(self, seed_type):
        """Obtenir les statistiques pour un type de graine"""
        url = f"{self.base_url}/stats/{seed_type}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête: {e}")
            return None
    
    def add_sensor_data(self, seed_type, temperature, soil_humidity, 
                       light_level, pH_du_sol, germination_score=None):
        """Ajouter des données de capteurs"""
        url = f"{self.base_url}/sensor-data"
        data = {
            "seed_type": seed_type,
            "temperature": temperature,
            "soil_humidity": soil_humidity,
            "light_level": light_level,
            "pH_du_sol": pH_du_sol,
            "germination_score": germination_score
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête: {e}")
            return None

def main():
    """Exemple d'utilisation du client"""
    print("🌱 Exemple d'utilisation de l'API de Prédiction de Germination\n")
    
    # Créer le client
    client = GerminationClient()
    
    # Exemple 1: Prédiction pour le maïs
    print("=" * 60)
    print("📊 PRÉDICTION POUR LE MAÏS")
    print("=" * 60)
    
    result = client.predict(
        seed_type="mais",
        temperature=25,
        soil_humidity=70,
        light_level=8,
        pH_du_sol=6.2
    )
    
    if result:
        print(f"\n✅ Score de germination prédit: {result['predicted_score']}")
        print(f"\n📋 Recommandations:")
        for rec in result['recommendations']:
            print(f"   • {rec}")
    
    # Exemple 2: Conditions optimales
    print("\n" + "=" * 60)
    print("🎯 CONDITIONS OPTIMALES POUR LE RIZ")
    print("=" * 60)
    
    conditions = client.get_optimal_conditions("riz")
    
    if conditions:
        print(f"\nType de graine: {conditions['seed_type']}")
        print(f"\nConditions optimales:")
        for param, values in conditions['optimal_conditions'].items():
            if isinstance(values, tuple):
                print(f"   • {param}: {values[0]} - {values[1]}")
            else:
                print(f"   • {param}: {values}")
    
    # Exemple 3: Ajouter des données de capteurs
    print("\n" + "=" * 60)
    print("💾 AJOUT DE DONNÉES DE CAPTEURS")
    print("=" * 60)
    
    result = client.add_sensor_data(
        seed_type="riz",
        temperature=28,
        soil_humidity=80,
        light_level=7,
        pH_du_sol=6.0,
        germination_score=95
    )
    
    if result:
        print(f"\n✅ {result['message']}")
        print(f"   ID: {result['id']}")
    
    # Exemple 4: Statistiques
    print("\n" + "=" * 60)
    print("📈 STATISTIQUES POUR LE MAÏS")
    print("=" * 60)
    
    stats = client.get_statistics("mais")
    
    if stats:
        print(f"\nNombre de prédictions: {stats['count']}")
        print(f"Score moyen: {stats['avg_score']}")
        print(f"Score minimum: {stats['min_score']}")
        print(f"Score maximum: {stats['max_score']}")
    
    print("\n" + "=" * 60)
    print("✅ Exemples terminés!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter à l'API.")
        print("   Assurez-vous que l'API est démarrée avec: python api.py")
    except Exception as e:
        print(f"❌ Erreur: {e}")
