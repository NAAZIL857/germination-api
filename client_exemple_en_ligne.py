# -*- coding: utf-8 -*-
"""
Exemple de client pour utiliser l'API deployee en ligne
Remplacez API_URL par votre URL Render
"""
import requests
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# REMPLACEZ PAR VOTRE URL DEPLOYEE
API_URL = "https://votre-api.onrender.com"  # Changez cette URL!

class GerminationAPIClient:
    """Client pour interagir avec l'API de germination deployee"""
    
    def __init__(self, api_url):
        self.api_url = api_url.rstrip('/')
    
    def predict(self, seed_type, temperature, soil_humidity, light_level, pH_du_sol):
        """Obtenir une prediction"""
        url = f"{self.api_url}/predict"
        data = {
            "seed_type": seed_type,
            "temperature": temperature,
            "soil_humidity": soil_humidity,
            "light_level": light_level,
            "pH_du_sol": pH_du_sol
        }
        
        try:
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")
            return None
    
    def get_conditions(self, seed_type=None):
        """Obtenir les conditions optimales"""
        if seed_type:
            url = f"{self.api_url}/conditions/{seed_type}"
        else:
            url = f"{self.api_url}/conditions"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")
            return None
    
    def get_stats(self, seed_type):
        """Obtenir les statistiques"""
        url = f"{self.api_url}/stats/{seed_type}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")
            return None

def main():
    print("="*70)
    print("  CLIENT API DE GERMINATION")
    print("="*70)
    
    # Creer le client
    client = GerminationAPIClient(API_URL)
    
    print(f"\nConnexion a: {API_URL}\n")
    
    # Exemple 1: Prediction pour tomate
    print("1. PREDICTION POUR TOMATE")
    print("-" * 70)
    result = client.predict(
        seed_type="tomate",
        temperature=25,
        soil_humidity=75,
        light_level=11,
        pH_du_sol=6.4
    )
    
    if result:
        print(f"Score: {result['predicted_score']}")
        print(f"Recommandations:")
        for rec in result['recommendations']:
            print(f"  - {rec}")
    
    # Exemple 2: Prediction pour laitue
    print("\n2. PREDICTION POUR LAITUE")
    print("-" * 70)
    result = client.predict(
        seed_type="laitue",
        temperature=15,
        soil_humidity=70,
        light_level=6,
        pH_du_sol=6.5
    )
    
    if result:
        print(f"Score: {result['predicted_score']}")
        print(f"Recommandations:")
        for rec in result['recommendations']:
            print(f"  - {rec}")
    
    # Exemple 3: Conditions optimales
    print("\n3. CONDITIONS OPTIMALES POUR CONCOMBRE")
    print("-" * 70)
    conditions = client.get_conditions("concombre")
    
    if conditions:
        print(f"Type: {conditions['seed_type']}")
        print(f"Conditions:")
        for param, values in conditions['optimal_conditions'].items():
            print(f"  - {param}: {values}")
    
    print("\n" + "="*70)
    print("  EXEMPLES TERMINES!")
    print("="*70)

if __name__ == "__main__":
    if API_URL == "https://votre-api.onrender.com":
        print("\n" + "!"*70)
        print("  ATTENTION: Vous devez modifier API_URL dans le script!")
        print("  Remplacez par votre URL Render")
        print("!"*70 + "\n")
    
    try:
        main()
    except Exception as e:
        print(f"\nErreur: {e}")
        print("\nVerifiez que:")
        print("  1. L'API est deployee")
        print("  2. L'URL est correcte")
        print("  3. Vous avez une connexion internet")
