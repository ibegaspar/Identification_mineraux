#!/usr/bin/env python3
"""
Script de test pour l'API Prédiction Minéraux
Team RobotMali - 2025
"""

import requests
import json
import time
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"  # Changez pour votre URL de déploiement

def test_health_check():
    """Test de l'endpoint de santé"""
    print("🔍 Test de l'endpoint /health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API en ligne - Modèle: {data.get('model_status', 'unknown')}")
            return True
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_root_endpoint():
    """Test de l'endpoint racine"""
    print("🔍 Test de l'endpoint /...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API active: {data.get('message', 'N/A')}")
            return True
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_predict_simple():
    """Test de prédiction simple (sans image)"""
    print("🔍 Test de prédiction simple...")
    
    test_cases = [
        {"durete": 7.0, "densite": 3.5, "expected": "Diamant"},
        {"durete": 6.0, "densite": 2.6, "expected": "Quartz"},
        {"durete": 5.0, "densite": 2.5, "expected": "Feldspath"},
        {"durete": 4.0, "densite": 2.2, "expected": "Calcite"},
        {"durete": 3.0, "densite": 2.0, "expected": "Gypse"},
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"  Test {i}: Dureté={test_case['durete']}, Densité={test_case['densite']}")
        
        try:
            form_data = {
                'durete': str(test_case['durete']),
                'densite': str(test_case['densite'])
            }
            
            response = requests.post(f"{API_BASE_URL}/predict_simple", data=form_data)
            
            if response.status_code == 200:
                data = response.json()
                predicted = data.get('predicted_mineral', 'Unknown')
                confidence = data.get('confidence', 0)
                
                if predicted == test_case['expected']:
                    print(f"    ✅ Prédiction correcte: {predicted} ({confidence:.1f}%)")
                else:
                    print(f"    ⚠️  Prédiction différente: {predicted} (attendu: {test_case['expected']})")
            else:
                print(f"    ❌ Erreur {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"    ❌ Erreur: {e}")
        
        time.sleep(0.5)  # Pause entre les tests

def test_predict_with_image():
    """Test de prédiction avec image"""
    print("🔍 Test de prédiction avec image...")
    
    # Chercher une image de test
    test_images = [
        "test_image.jpg",
        "mineral_test.jpg", 
        "sample.jpg"
    ]
    
    image_found = None
    for img_name in test_images:
        if Path(img_name).exists():
            image_found = img_name
            break
    
    if not image_found:
        print("  ⚠️  Aucune image de test trouvée. Créez un fichier 'test_image.jpg' pour tester.")
        return
    
    print(f"  Utilisation de l'image: {image_found}")
    
    try:
        with open(image_found, 'rb') as f:
            files = {'image': f}
            data = {
                'durete': '7.0',
                'densite': '3.5'
            }
            
            response = requests.post(f"{API_BASE_URL}/predict", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ Prédiction réussie:")
                print(f"     Minéral: {result.get('predicted_mineral', 'Unknown')}")
                print(f"     Confiance: {result.get('confidence', 0):.1f}%")
                print(f"     Méthode: IA complète")
            else:
                print(f"  ❌ Erreur {response.status_code}: {response.text}")
                
    except Exception as e:
        print(f"  ❌ Erreur: {e}")

def test_error_handling():
    """Test de gestion d'erreurs"""
    print("🔍 Test de gestion d'erreurs...")
    
    # Test avec valeurs invalides
    invalid_cases = [
        {"durete": -1, "densite": 3.5, "expected_error": "Dureté doit être entre 0 et 10"},
        {"durete": 11, "densite": 3.5, "expected_error": "Dureté doit être entre 0 et 10"},
        {"durete": 7.0, "densite": -1, "expected_error": "Densité doit être entre 0 et 20"},
        {"durete": 7.0, "densite": 21, "expected_error": "Densité doit être entre 0 et 20"},
    ]
    
    for i, test_case in enumerate(invalid_cases, 1):
        print(f"  Test d'erreur {i}: Dureté={test_case['durete']}, Densité={test_case['densite']}")
        
        try:
            form_data = {
                'durete': str(test_case['durete']),
                'densite': str(test_case['densite'])
            }
            
            response = requests.post(f"{API_BASE_URL}/predict_simple", data=form_data)
            
            if response.status_code == 400:
                data = response.json()
                error_msg = data.get('detail', '')
                if test_case['expected_error'] in error_msg:
                    print(f"    ✅ Erreur correctement gérée: {error_msg}")
                else:
                    print(f"    ⚠️  Message d'erreur différent: {error_msg}")
            else:
                print(f"    ❌ Erreur attendue non reçue (status: {response.status_code})")
                
        except Exception as e:
            print(f"    ❌ Erreur: {e}")
        
        time.sleep(0.5)

def main():
    """Fonction principale de test"""
    print("🚀 Démarrage des tests de l'API Prédiction Minéraux")
    print("=" * 50)
    
    # Tests de base
    if not test_root_endpoint():
        print("❌ L'API n'est pas accessible. Arrêt des tests.")
        return
    
    if not test_health_check():
        print("⚠️  L'API est accessible mais les modèles ne sont pas chargés.")
    
    print("\n" + "=" * 50)
    
    # Tests de prédiction
    test_predict_simple()
    
    print("\n" + "=" * 50)
    
    # Test avec image
    test_predict_with_image()
    
    print("\n" + "=" * 50)
    
    # Tests d'erreurs
    test_error_handling()
    
    print("\n" + "=" * 50)
    print("✅ Tests terminés !")
    print("\n📱 Pour tester avec l'application mobile:")
    print("1. Déployez l'API sur un serveur")
    print("2. Modifiez API_BASE_URL dans mobile_app/App.js")
    print("3. Lancez l'application mobile")

if __name__ == "__main__":
    main() 