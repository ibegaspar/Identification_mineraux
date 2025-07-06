# API Prédiction Minéraux - Team RobotMali

API FastAPI pour identifier les minéraux à partir d'images et de propriétés physiques.

## 🚀 Installation

```bash
pip install -r requirements_api.txt
```

## 🏃‍♂️ Lancement local

```bash
python api.py
```

L'API sera accessible sur : http://localhost:8000

## 📚 Documentation automatique

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🔗 Endpoints

### 1. Test de l'API
```
GET /
```
Retourne un message de bienvenue.

### 2. Vérification de l'état
```
GET /health
```
Vérifie l'état de l'API et des modèles.

### 3. Prédiction complète (avec image)
```
POST /predict
```
**Paramètres :**
- `image` : Fichier image (JPG, PNG)
- `durete` : Dureté sur l'échelle de Mohs (0-10)
- `densite` : Densité en g/cm³ (0-20)

### 4. Prédiction simple (sans image)
```
POST /predict_simple
```
**Paramètres :**
- `durete` : Dureté sur l'échelle de Mohs (0-10)
- `densite` : Densité en g/cm³ (0-20)

## 📱 Utilisation avec une application mobile

### Exemple de requête (JavaScript/React Native)
```javascript
const formData = new FormData();
formData.append('image', imageFile);
formData.append('durete', '7.0');
formData.append('densite', '3.5');

const response = await fetch('https://votre-api.com/predict', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result.predicted_mineral);
```

### Exemple de requête simple (sans image)
```javascript
const formData = new FormData();
formData.append('durete', '7.0');
formData.append('densite', '3.5');

const response = await fetch('https://votre-api.com/predict_simple', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result.predicted_mineral);
```

## 🚀 Déploiement

### Railway
1. Connectez votre repository GitHub
2. Utilisez `requirements_api.txt` comme fichier de dépendances
3. Déployez automatiquement

### Render
1. Créez un nouveau Web Service
2. Connectez votre repository
3. Commande de build : `pip install -r requirements_api.txt`
4. Commande de démarrage : `uvicorn api:app --host 0.0.0.0 --port $PORT`

### Heroku
1. Créez une nouvelle app
2. Connectez votre repository
3. Le `Procfile` sera automatiquement détecté

## 📊 Réponse de l'API

### Succès
```json
{
  "success": true,
  "predicted_mineral": "Diamant",
  "confidence": 95.2,
  "input_data": {
    "durete": 7.0,
    "densite": 3.5,
    "image_size": "380x380"
  },
  "model_info": {
    "model_loaded": true,
    "prediction_time": "real-time"
  }
}
```

### Erreur
```json
{
  "detail": "Dureté doit être entre 0 et 10"
}
```

## 🔧 Configuration

L'API nécessite les fichiers suivants dans le même répertoire :
- `model_final_durete_densiter.h5` : Modèle TensorFlow
- `scaler.pkl` : Scaler pour normalisation
- `label_encoder.pkl` : Encodeur de labels

## 👥 Équipe

**Team RobotMali** - 2025

---

*Cette API utilise un modèle de deep learning pour la classification de minéraux.* 