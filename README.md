# 🔬 Prédiction Minéraux - Team RobotMali

Système complet de prédiction de minéraux utilisant l'IA avec API FastAPI et application mobile React Native.

## 📋 Vue d'ensemble

Ce projet comprend :
- **API FastAPI** : Backend avec modèle TensorFlow pour la prédiction
- **Application mobile React Native** : Interface utilisateur pour smartphones
- **Modèle IA** : Classification de minéraux basée sur images et propriétés physiques

## 🚀 Démarrage rapide

### Option 1: Déploiement automatique (Recommandé)

```powershell
# Windows
.\deploy.ps1 railway

# Linux/Mac
./deploy.sh railway
```

### Option 2: Test local

```powershell
# Windows
.\deploy.ps1 local

# Linux/Mac
./deploy.sh local
```

## 📁 Structure du projet

```
Mon IA/
├── api.py                    # API FastAPI principale
├── requirements_api.txt      # Dépendances Python pour l'API
├── test_api.py              # Script de test de l'API
├── Procfile                 # Configuration pour Heroku
├── railway.json             # Configuration Railway
├── deploy.ps1               # Script de déploiement Windows
├── deploy.sh                # Script de déploiement Linux/Mac
├── DEPLOIEMENT.md           # Guide de déploiement complet
├── README_API.md            # Documentation de l'API
├── mobile_app/              # Application mobile React Native
│   ├── App.js               # Application principale
│   ├── package.json         # Dépendances Node.js
│   └── README.md            # Documentation mobile
├── model_final_durete_densiter.h5  # Modèle TensorFlow
├── scaler.pkl               # Scaler pour normalisation
├── label_encoder.pkl        # Encodeur de labels
└── projet.py                # Application Streamlit (originale)
```

## 🖥️ API FastAPI

### Fonctionnalités
- **Prédiction complète** : Image + propriétés physiques
- **Prédiction simple** : Propriétés physiques uniquement
- **Documentation automatique** : Swagger UI et ReDoc
- **Gestion d'erreurs** : Validation et messages d'erreur clairs

### Endpoints
- `GET /` : Test de l'API
- `GET /health` : État de l'API et des modèles
- `POST /predict` : Prédiction avec image
- `POST /predict_simple` : Prédiction sans image

### Déploiement
```bash
# Installation
pip install -r requirements_api.txt

# Lancement local
python api.py

# Test
python test_api.py
```

## 📱 Application Mobile

### Fonctionnalités
- **Prise de photo** : Utilisation de l'appareil photo
- **Sélection d'image** : Choix depuis la galerie
- **Saisie des propriétés** : Dureté et densité
- **Interface moderne** : Design responsive et intuitif

### Installation
```bash
cd mobile_app
npm install
npm run android  # ou npm run ios
```

### Configuration
Modifiez `API_BASE_URL` dans `mobile_app/App.js` :
```javascript
const API_BASE_URL = 'https://votre-api-deployee.com';
```

## 🔧 Configuration

### Prérequis
- Python 3.8+
- Node.js 16+
- Git
- Fichiers de modèle : `*.h5`, `*.pkl`

### Variables d'environnement
```bash
# API
PYTHON_VERSION=3.10
PORT=8000

# Mobile (optionnel)
API_BASE_URL=https://votre-api.com
```

## 🚀 Déploiement

### Plateformes supportées

| Plateforme | Gratuit | Facile | Recommandé |
|------------|---------|--------|------------|
| Railway    | ✅      | ✅     | ⭐⭐⭐⭐⭐ |
| Render     | ✅      | ✅     | ⭐⭐⭐⭐ |
| Heroku     | ❌      | ✅     | ⭐⭐⭐ |
| VPS        | ❌      | ❌     | ⭐⭐ |

### Déploiement automatique
```powershell
# Railway (recommandé)
.\deploy.ps1 railway

# Render
.\deploy.ps1 render

# Heroku
.\deploy.ps1 heroku

# Tout (test + déploiement + config mobile)
.\deploy.ps1 all
```

## 📊 Utilisation

### 1. Déployer l'API
```powershell
.\deploy.ps1 railway
```

### 2. Configurer l'application mobile
```bash
cd mobile_app
# Modifier API_BASE_URL dans App.js
npm install
```

### 3. Tester l'application
```bash
# Test API
python test_api.py

# Test mobile
cd mobile_app
npm run android
```

## 🔍 Monitoring

### Logs de l'API
```bash
# Railway
railway logs

# Render
# Dashboard web

# Heroku
heroku logs --tail
```

### Métriques importantes
- **Temps de réponse** : < 2 secondes
- **Disponibilité** : > 99%
- **Erreurs** : < 1%

## 🚨 Dépannage

### Problèmes courants

1. **API ne démarre pas**
   ```bash
   pip install -r requirements_api.txt
   python api.py
   ```

2. **Modèles non trouvés**
   ```bash
   ls -la *.h5 *.pkl
   ```

3. **Application mobile ne se connecte pas**
   ```javascript
   console.log('API URL:', API_BASE_URL);
   ```

### Support
- **Documentation API** : `README_API.md`
- **Documentation Mobile** : `mobile_app/README.md`
- **Guide de déploiement** : `DEPLOIEMENT.md`

## 📈 Améliorations futures

- [ ] Base de données pour l'historique
- [ ] Authentification utilisateur
- [ ] Mode hors ligne
- [ ] Support de plus de minéraux
- [ ] Interface web admin
- [ ] Notifications push

## 👥 Équipe

**Team RobotMali** - 2025

### Contributeurs
- Développement API
- Développement mobile
- Modèle IA
- Documentation

## 📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

---

## 🎯 Prochaines étapes

1. **Déployer l'API** sur Railway
2. **Tester l'API** avec le script de test
3. **Configurer l'application mobile**
4. **Tester l'application mobile**
5. **Publier sur les stores**

**Bonne chance avec votre projet de prédiction de minéraux ! 🚀** 