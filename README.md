# Application de Prédiction de Minéraux

Cette application Streamlit permet de prédire le type de minéral en analysant une image et en utilisant les propriétés physiques (dureté et densité).

## 🚀 Déploiement

### Option 1: Déploiement sur Streamlit Cloud (Recommandé)

1. **Préparez votre repository GitHub :**
   - Créez un repository GitHub
   - Uploadez tous les fichiers du projet
   - Assurez-vous que les fichiers suivants sont présents :
     - `projet.py` (application principale)
     - `requirements.txt` (dépendances)
     - `model_final_durete_densiter.h5` (modèle entraîné)
     - `scaler.pkl` (scaler pour les données)
     - `label_encoder.pkl` (encodeur de labels)

2. **Déployez sur Streamlit Cloud :**
   - Allez sur [share.streamlit.io](https://share.streamlit.io)
   - Connectez-vous avec votre compte GitHub
   - Cliquez sur "New app"
   - Sélectionnez votre repository et le fichier `projet.py`
   - Cliquez sur "Deploy"

### Option 2: Déploiement local

1. **Installez les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

2. **Lancez l'application :**
   ```bash
   streamlit run projet.py
   ```

### Option 3: Déploiement sur Heroku

1. **Créez un fichier `Procfile` :**
   ```
   web: streamlit run projet.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Créez un fichier `setup.sh` :**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **Déployez sur Heroku :**
   ```bash
   heroku create votre-app-name
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

## 📁 Structure du projet

```
Mon IA/
├── projet.py                    # Application principale
├── requirements.txt             # Dépendances Python
├── .streamlit/
│   └── config.toml             # Configuration Streamlit
├── model_final_durete_densiter.h5  # Modèle entraîné
├── scaler.pkl                  # Scaler pour normalisation
├── label_encoder.pkl           # Encodeur de labels
├── mineral_data.csv            # Données d'entraînement
├── data_test.csv               # Données de test
└── README.md                   # Ce fichier
```

## 🔧 Configuration

L'application nécessite les fichiers suivants dans le même répertoire :
- `model_final_durete_densiter.h5` : Modèle Keras entraîné
- `scaler.pkl` : Scaler pour normaliser les données d'entrée
- `label_encoder.pkl` : Encodeur pour convertir les prédictions en noms de minéraux

## 📝 Utilisation

1. Prenez une photo ou importez une image de minéral
2. Saisissez la dureté du minéral (échelle de Mohs)
3. Saisissez la densité du minéral (g/cm³)
4. Cliquez sur "Prédire le minéral"
5. Consultez le résultat et la confiance de la prédiction

## 🛠️ Technologies utilisées

- **Streamlit** : Interface utilisateur
- **TensorFlow/Keras** : Modèle de deep learning
- **OpenCV** : Traitement d'images
- **Scikit-learn** : Prétraitement des données
- **NumPy/Pandas** : Manipulation des données

## 👥 Équipe

**Team RobotMali** - 2025

---

*Cette application utilise un modèle de deep learning pour la classification de minéraux basée sur l'analyse d'images et les propriétés physiques.* 