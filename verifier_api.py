# -*- coding: utf-8 -*-
"""Script simple pour vérifier si l'API fonctionne"""
import requests
import time
import sys

def verifier_api():
    print("Verification de l'API...")
    print("-" * 50)
    
    urls = [
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    for url in urls:
        try:
            print(f"\nTest de connexion a: {url}")
            response = requests.get(f"{url}/health", timeout=5)
            
            if response.status_code == 200:
                print(f"  [OK] L'API est accessible!")
                print(f"  Status: {response.json()}")
                print(f"\n" + "="*50)
                print(f"L'API fonctionne correctement!")
                print(f"Ouvrez votre navigateur a: {url}")
                print(f"Documentation: {url}/docs")
                print("="*50)
                return True
        except requests.exceptions.ConnectionError:
            print(f"  [ERREUR] Impossible de se connecter")
        except Exception as e:
            print(f"  [ERREUR] {e}")
    
    print("\n" + "="*50)
    print("L'API n'est pas accessible!")
    print("\nPour demarrer l'API:")
    print("  1. Ouvrez un terminal")
    print("  2. Executez: python api.py")
    print("     OU double-cliquez sur: start_api.bat")
    print("  3. Attendez le message de demarrage")
    print("  4. Ouvrez: http://localhost:8000")
    print("="*50)
    return False

if __name__ == "__main__":
    verifier_api()
