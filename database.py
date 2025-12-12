# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class GerminationDatabase:
    def __init__(self, db_path='germination.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données avec les tables nécessaires"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table pour les données de capteurs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seed_type TEXT NOT NULL,
                temperature REAL NOT NULL,
                soil_humidity REAL NOT NULL,
                air_humidity REAL NOT NULL,
                light_level REAL NOT NULL,
                germination_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table pour l'historique des prédictions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seed_type TEXT NOT NULL,
                temperature REAL NOT NULL,
                soil_humidity REAL NOT NULL,
                air_humidity REAL NOT NULL,
                light_level REAL NOT NULL,
                predicted_score REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_sensor_data(self, seed_type: str, temperature: float, soil_humidity: float,
                       air_humidity: float, light_level: float, germination_score: Optional[float] = None):
        """Ajoute des données de capteurs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sensor_data (seed_type, temperature, soil_humidity, air_humidity, light_level, germination_score)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (seed_type, temperature, soil_humidity, air_humidity, light_level, germination_score))
        
        conn.commit()
        data_id = cursor.lastrowid
        conn.close()
        return data_id
    
    def add_prediction(self, seed_type: str, temperature: float, soil_humidity: float,
                      air_humidity: float, light_level: float, predicted_score: float):
        """Enregistre une prédiction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions (seed_type, temperature, soil_humidity, air_humidity, light_level, predicted_score)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (seed_type, temperature, soil_humidity, air_humidity, light_level, predicted_score))
        
        conn.commit()
        pred_id = cursor.lastrowid
        conn.close()
        return pred_id
    
    def get_sensor_data(self, limit: int = 100) -> List[Dict]:
        """Récupère les données de capteurs"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_predictions(self, limit: int = 100) -> List[Dict]:
        """Récupère l'historique des prédictions"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM predictions ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_stats_by_seed_type(self, seed_type: str) -> Dict:
        """Récupère les statistiques pour un type de graine"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as count,
                AVG(predicted_score) as avg_score,
                MIN(predicted_score) as min_score,
                MAX(predicted_score) as max_score
            FROM predictions
            WHERE seed_type = ?
        ''', (seed_type,))
        
        row = cursor.fetchone()
        conn.close()
        
        return {
            'seed_type': seed_type,
            'count': row[0],
            'avg_score': round(row[1], 2) if row[1] else 0,
            'min_score': round(row[2], 2) if row[2] else 0,
            'max_score': round(row[3], 2) if row[3] else 0
        }
