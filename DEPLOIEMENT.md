# 🚀 Guide de Déploiement - API + Application Mobile

Guide complet pour déployer l'API FastAPI et l'application mobile React Native.

## 📋 Table des matières

1. [Déploiement de l'API](#déploiement-de-lapi)
2. [Déploiement de l'Application Mobile](#déploiement-de-lapplication-mobile)
3. [Configuration et Tests](#configuration-et-tests)
4. [Maintenance](#maintenance)

---

## 🖥️ Déploiement de l'API

### Option 1: Railway (Recommandé)

**Avantages :** Gratuit, simple, déploiement automatique

1. **Créer un compte Railway**
   - Allez sur [railway.app](https://railway.app)
   - Connectez-vous avec GitHub

2. **Connecter le repository**
   - Cliquez sur "New Project"
   - Sélectionnez "Deploy from GitHub repo"
   - Choisissez votre repository

3. **Configuration**
   - Railway détectera automatiquement que c'est une application Python
   - Utilisez `requirements_api.txt` comme fichier de dépendances
   - Le `Procfile` sera automatiquement détecté

4. **Variables d'environnement (optionnel)**
   ```bash
   PYTHON_VERSION=3.10
   PORT=8000
   ```

5. **Déploiement**
   - Railway déploiera automatiquement à chaque push
   - L'URL sera fournie dans le dashboard

### Option 2: Render

**Avantages :** Gratuit, fiable, bonnes performances

1. **Créer un compte Render**
   - Allez sur [render.com](https://render.com)
   - Connectez-vous avec GitHub

2. **Créer un Web Service**
   - Cliquez sur "New +" → "Web Service"
   - Connectez votre repository GitHub

3. **Configuration**
   ```
   Name: mineral-prediction-api
   Environment: Python 3
   Build Command: pip install -r requirements_api.txt
   Start Command: uvicorn api:app --host 0.0.0.0 --port $PORT
   ```

4. **Déploiement**
   - Cliquez sur "Create Web Service"
   - Render déploiera automatiquement

### Option 3: Heroku

**Avantages :** Très populaire, bonne documentation

1. **Installer Heroku CLI**
   ```bash
   # Windows
   winget install --id=Heroku.HerokuCLI
   
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Créer une app Heroku**
   ```bash
   heroku login
   heroku create mineral-prediction-api
   ```

3. **Déployer**
   ```bash
   git add .
   git commit -m "Deploy API"
   git push heroku main
   ```

4. **Vérifier le déploiement**
   ```bash
   heroku logs --tail
   ```

### Option 4: VPS (Serveur Virtuel)

**Avantages :** Contrôle total, meilleures performances

1. **Créer un VPS**
   - DigitalOcean, AWS, Google Cloud, etc.
   - Ubuntu 20.04 ou 22.04 recommandé

2. **Installation des dépendances**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   ```

3. **Cloner le projet**
   ```bash
   git clone https://github.com/votre-username/votre-repo.git
   cd votre-repo
   pip3 install -r requirements_api.txt
   ```

4. **Configuration systemd**
   ```bash
   sudo nano /etc/systemd/system/mineral-api.service
   ```
   
   Contenu :
   ```ini
   [Unit]
   Description=Mineral Prediction API
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/votre-repo
   Environment="PATH=/home/ubuntu/votre-repo/venv/bin"
   ExecStart=/home/ubuntu/votre-repo/venv/bin/uvicorn api:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. **Démarrer le service**
   ```bash
   sudo systemctl enable mineral-api
   sudo systemctl start mineral-api
   ```

---

## 📱 Déploiement de l'Application Mobile

### Préparation

1. **Installer les outils**
   ```bash
   npm install -g @react-native-community/cli
   npm install -g expo-cli  # Optionnel, pour Expo
   ```

2. **Cloner et configurer**
   ```bash
   cd mobile_app
   npm install
   ```

### Option 1: React Native CLI (Recommandé)

#### Android

1. **Configuration Android Studio**
   - Installer Android Studio
   - Configurer un émulateur ou connecter un appareil

2. **Générer l'APK**
   ```bash
   cd android
   ./gradlew assembleRelease
   ```

3. **APK de debug (pour tests)**
   ```bash
   npx react-native run-android
   ```

#### iOS (Mac uniquement)

1. **Configuration Xcode**
   - Installer Xcode depuis l'App Store
   - Installer les outils de ligne de commande

2. **Lancer sur simulateur**
   ```bash
   npx react-native run-ios
   ```

3. **Build pour App Store**
   - Ouvrir le projet dans Xcode
   - Configurer les certificats
   - Archiver et distribuer

### Option 2: Expo (Plus simple)

1. **Créer un projet Expo**
   ```bash
   npx create-expo-app MineralPredictionApp
   cd MineralPredictionApp
   ```

2. **Copier le code**
   - Copier le contenu de `mobile_app/App.js`
   - Installer les dépendances nécessaires

3. **Déployer**
   ```bash
   expo build:android  # Pour Android
   expo build:ios      # Pour iOS
   ```

---

## 🔧 Configuration et Tests

### 1. Tester l'API

```bash
# Test local
python test_api.py

# Test avec curl
curl -X GET "https://votre-api.com/health"
```

### 2. Configurer l'application mobile

Modifiez `mobile_app/App.js` :
```javascript
const API_BASE_URL = 'https://votre-api-deployee.com';
```

### 3. Tests de l'application mobile

```bash
cd mobile_app
npm test
```

---

## 🔍 Monitoring et Maintenance

### Logs de l'API

```bash
# Railway
railway logs

# Render
# Disponible dans le dashboard

# Heroku
heroku logs --tail

# VPS
sudo journalctl -u mineral-api -f
```

### Métriques importantes

- **Temps de réponse** : < 2 secondes
- **Disponibilité** : > 99%
- **Erreurs** : < 1%

### Sauvegarde

```bash
# Sauvegarder les modèles
tar -czf models_backup.tar.gz *.h5 *.pkl

# Sauvegarder la base de données (si applicable)
pg_dump your_database > backup.sql
```

---

## 🚨 Dépannage

### Problèmes courants

1. **API ne démarre pas**
   ```bash
   # Vérifier les logs
   heroku logs --tail
   
   # Vérifier les dépendances
   pip install -r requirements_api.txt
   ```

2. **Erreur de modèle**
   ```bash
   # Vérifier que les fichiers sont présents
   ls -la *.h5 *.pkl
   
   # Vérifier les permissions
   chmod 644 *.h5 *.pkl
   ```

3. **Application mobile ne se connecte pas**
   ```javascript
   // Vérifier l'URL de l'API
   console.log('API URL:', API_BASE_URL);
   
   // Tester la connexion
   fetch(`${API_BASE_URL}/health`)
     .then(response => console.log('Status:', response.status))
     .catch(error => console.error('Error:', error));
   ```

### Support

- **Documentation FastAPI** : https://fastapi.tiangolo.com/
- **Documentation React Native** : https://reactnative.dev/
- **Railway Support** : https://docs.railway.app/
- **Render Support** : https://render.com/docs

---

## 📊 Coûts estimés

| Service | Plan gratuit | Plan payant |
|---------|-------------|-------------|
| Railway | ✅ Illimité | $5-20/mois |
| Render | ✅ 750h/mois | $7-25/mois |
| Heroku | ❌ Discontinué | $7-25/mois |
| VPS | ❌ | $5-20/mois |

---

## 🎯 Prochaines étapes

1. **Déployer l'API** sur Railway ou Render
2. **Tester l'API** avec le script de test
3. **Configurer l'application mobile** avec l'URL de l'API
4. **Tester l'application mobile** sur un émulateur
5. **Publier l'application** sur les stores

---

**Team RobotMali** - 2025

*Ce guide vous accompagne dans le déploiement complet de votre solution de prédiction de minéraux.* 