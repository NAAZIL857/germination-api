# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.linear_model import LinearRegression

def light_percent_to_hours(light_percent):
    """
    Convertit un pourcentage de luminosité (0-100%) en heures équivalentes (0-14h)
    Basé sur une journée maximale de 14h de lumière
    """
    return (light_percent / 100) * 14

# --- Base de connaissances des conditions optimales ---
OPTIMAL_CONDITIONS = {
    'mais': {
        'temperature': (18, 30),
        'soil_humidity': (60, 80),
        'air_humidity': (50, 70),
        'light_level': (6, 10)
    },
    'riz': {
        'temperature': (20, 35),
        'soil_humidity': (70, 90),
        'air_humidity': (60, 80),
        'light_level': (5, 9)
    },
    'ble': {
        'temperature': (15, 25),
        'soil_humidity': (50, 70),
        'air_humidity': (40, 60),
        'light_level': (6, 10)
    },
    'soja': {
        'temperature': (20, 30),
        'soil_humidity': (60, 75),
        'air_humidity': (50, 70),
        'light_level': (7, 12)
    },
    'tomate': {
        'temperature': (20, 30),
        'soil_humidity': (65, 85),
        'air_humidity': (60, 80),
        'light_level': (8, 14)
    },
    'haricot': {
        'temperature': (18, 28),
        'soil_humidity': (60, 80),
        'air_humidity': (50, 70),
        'light_level': (6, 10)
    },
    'carotte': {
        'temperature': (15, 25),
        'soil_humidity': (55, 75),
        'air_humidity': (45, 65),
        'light_level': (5, 8)
    },
    'laitue': {
        'temperature': (10, 20),
        'soil_humidity': (60, 80),
        'air_humidity': (50, 70),
        'light_level': (4, 8)
    },
    'concombre': {
        'temperature': (20, 30),
        'soil_humidity': (70, 90),
        'air_humidity': (60, 80),
        'light_level': (8, 12)
    },
    'poivron': {
        'temperature': (22, 30),
        'soil_humidity': (65, 85),
        'air_humidity': (60, 80),
        'light_level': (8, 14)
    }
}

RECOMMENDATIONS_PH = {
    'low': "Le pH du sol est trop bas. Ajoutez de la chaux agricole ou de la cendre pour réduire l’acidité.",
    'high': "Le pH du sol est trop élevé. Ajoutez du compost, du fumier ou du sulfate d’ammonium pour acidifier légèrement le sol."
}

def train_germination_model(data_path='sensors_data.csv'):
    """
    Entraîne un modèle pour prédire le score de germination en prenant
    en compte le type de graine comme une caractéristique.
    """
    try:
        # 1. Charger les données
        df = pd.read_csv(data_path)
        
        # Valider les colonnes requises
        required_columns = ['seed_type', 'temperature', 'soil_humidity', 'air_humidity', 'light_level', 'germination_score']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Colonnes manquantes dans le fichier: {missing_columns}")

        # 2. Préparer les features (X) et la cible (y)
        # On transforme 'seed_type' en variables numériques (One-Hot Encoding)
        features_df = pd.get_dummies(df[['seed_type', 'temperature', 'soil_humidity', 'air_humidity', 'light_level']], columns=['seed_type'])
        target = df['germination_score']
        
        # 3. Entraîner le modèle
        model = LinearRegression()
        model.fit(features_df, target)
        
        print("[OK] Modele d'IA multi-graines entraine avec succes.")
        # Retourner le modèle et les colonnes de features pour la prédiction
        return model, features_df.columns
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier de données introuvable: {data_path}")
    except Exception as e:
        raise Exception(f"Erreur lors de l'entraînement du modèle: {str(e)}")

def get_recommendations(seed_type, temperature, soil_humidity, air_humidity, light_level):
    """
    Analyse les données des capteurs pour un type de graine spécifique et retourne des recommandations.
    
    Args:
        seed_type: Type de graine
        temperature: Température en °C
        soil_humidity: Humidité du sol en %
        air_humidity: Humidité de l'air en %
        light_level: Niveau de lumière en % (0-100)
    """
    if seed_type not in OPTIMAL_CONDITIONS:
        return [f"[ERREUR] Type de graine '{seed_type}' non reconnu."]

    # Convertir le pourcentage de lumière en heures équivalentes
    light_hours = light_percent_to_hours(light_level)

    conditions = OPTIMAL_CONDITIONS[seed_type]
    recommendations = []
    
    # Analyse de chaque paramètre
    min_temp, max_temp = conditions['temperature']
    if temperature < min_temp:
        recommendations.append(f"[TEMPERATURE] Trop basse. Ideal: {min_temp}-{max_temp}C.")
    elif temperature > max_temp:
        recommendations.append(f"[TEMPERATURE] Trop elevee. Ideal: {min_temp}-{max_temp}C.")

    min_hum, max_hum = conditions['soil_humidity']
    if soil_humidity < min_hum:
        recommendations.append(f"[HUMIDITE] Sol trop sec. Ideal: {min_hum}-{max_hum}%")
    elif soil_humidity > max_hum:
        recommendations.append(f"[HUMIDITE] Sol trop humide. Ideal: {min_hum}-{max_hum}%")

    min_light, max_light = conditions['light_level']
    if light_hours < min_light:
        min_percent = int((min_light / 14) * 100)
        max_percent = int((max_light / 14) * 100)
        recommendations.append(f"[LUMIERE] Insuffisante ({light_level}%). Ideal: {min_percent}-{max_percent}%")
    elif light_hours > max_light:
        min_percent = int((min_light / 14) * 100)
        max_percent = int((max_light / 14) * 100)
        recommendations.append(f"[LUMIERE] Excessive ({light_level}%). Ideal: {min_percent}-{max_percent}%")

    min_air, max_air = conditions['air_humidity']
    if air_humidity < min_air:
        recommendations.append(f"[HUMIDITE AIR] Trop basse. Ideal: {min_air}-{max_air}%")
    elif air_humidity > max_air:
        recommendations.append(f"[HUMIDITE AIR] Trop elevee. Ideal: {min_air}-{max_air}%")

    if not recommendations:
        recommendations.append(f"[OK] Conditions optimales pour le {seed_type}.")
        
    return recommendations

def predict_score(model, model_columns, data):
    """
    Prépare les données pour la prédiction en s'assurant que les colonnes correspondent
    à celles utilisées pour l'entraînement.
    """
    # Convertir light_level de % en heures pour le modèle
    data_copy = data.copy()
    if 'light_level' in data_copy:
        data_copy['light_level'] = light_percent_to_hours(data_copy['light_level'])
    
    # Crée un DataFrame pour les nouvelles données
    df = pd.DataFrame([data_copy])
    # Applique le One-Hot Encoding
    df_encoded = pd.get_dummies(df)
    # Réaligne les colonnes sur celles du modèle, en ajoutant les colonnes manquantes avec 0
    df_aligned = df_encoded.reindex(columns=model_columns, fill_value=0)
    # Fait la prédiction
    return model.predict(df_aligned)

# --- Point d'entrée du script ---
if __name__ == "__main__":
    # Entraîner le modèle au démarrage
    model, model_columns = train_germination_model('sensors_data.csv')
    
    print("\n--- Simulation de l'analyse pour différents types de graines ---")
    
    # Exemple 1: Maïs avec de mauvaises conditions
    print("\nCas 1: Maïs, conditions non optimales")
    data_mais = {
        'seed_type': 'mais',
        'temperature': 16, 
        'soil_humidity': 55,
        'air_humidity': 45,
        'light_level': 30
    }
    
    score_mais = predict_score(model, model_columns, data_mais)
    print(f"Score de germination prédit: {score_mais[0]:.2f}")
    
    recs_mais = get_recommendations(**data_mais)
    print("Recommandations:")
    for rec in recs_mais:
        print(f"- {rec}")

    # Exemple 2: Riz avec de bonnes conditions
    print("\nCas 2: Riz, conditions optimales")
    data_riz = {
        'seed_type': 'riz',
        'temperature': 28, 
        'soil_humidity': 80,
        'air_humidity': 70,
        'light_level': 50
    }
    
    score_riz = predict_score(model, model_columns, data_riz)
    print(f"Score de germination prédit: {score_riz[0]:.2f}")
    
    recs_riz = get_recommendations(**data_riz)
    print("Recommandations:")
    for rec in recs_riz:
        print(f"- {rec}")