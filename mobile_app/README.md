# 📱 Application Mobile - Prédiction Minéraux

Application React Native pour identifier les minéraux en utilisant l'API FastAPI.

## 🚀 Installation

### Prérequis
- Node.js (version 16 ou supérieure)
- React Native CLI
- Android Studio (pour Android)
- Xcode (pour iOS, Mac uniquement)

### Installation des dépendances
```bash
cd mobile_app
npm install
```

### Configuration de l'API
Modifiez la variable `API_BASE_URL` dans `App.js` :
```javascript
const API_BASE_URL = 'https://votre-api-deployee.com'; // Remplacez par votre URL
```

## 🏃‍♂️ Lancement

### Android
```bash
npm run android
```

### iOS
```bash
npm run ios
```

### Démarrage du serveur Metro
```bash
npm start
```

## 📱 Fonctionnalités

### 🔬 Prédiction de minéraux
- **Prise de photo** : Utilisez l'appareil photo pour capturer un minéral
- **Sélection d'image** : Choisissez une image depuis la galerie
- **Saisie des propriétés** : Entrez la dureté et la densité
- **Prédiction IA** : Obtenez le résultat avec un niveau de confiance

### 📊 Interface utilisateur
- **Design moderne** : Interface intuitive et responsive
- **Validation des données** : Vérification des valeurs saisies
- **Gestion d'erreurs** : Messages d'erreur clairs
- **Indicateurs de chargement** : Feedback visuel pendant les requêtes

## 🔧 Configuration des permissions

### Android
Ajoutez dans `android/app/src/main/AndroidManifest.xml` :
```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.INTERNET" />
```

### iOS
Ajoutez dans `ios/YourApp/Info.plist` :
```xml
<key>NSCameraUsageDescription</key>
<string>Cette application nécessite l'accès à la caméra pour photographier les minéraux</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>Cette application nécessite l'accès à la galerie pour sélectionner des images de minéraux</string>
```

## 📡 Communication avec l'API

### Endpoints utilisés
- `POST /predict` : Prédiction avec image + propriétés physiques
- `POST /predict_simple` : Prédiction avec propriétés physiques uniquement

### Format des requêtes
```javascript
// Avec image
const formData = new FormData();
formData.append('image', imageFile);
formData.append('durete', '7.0');
formData.append('densite', '3.5');

// Sans image
const formData = new FormData();
formData.append('durete', '7.0');
formData.append('densite', '3.5');
```

### Format des réponses
```json
{
  "success": true,
  "predicted_mineral": "Diamant",
  "confidence": 95.2,
  "input_data": {
    "durete": 7.0,
    "densite": 3.5,
    "image_size": "380x380"
  }
}
```

## 🎨 Personnalisation

### Couleurs
Modifiez les couleurs dans `App.js` :
```javascript
const styles = StyleSheet.create({
  // Couleurs principales
  primaryColor: '#27AE60',
  secondaryColor: '#3498DB',
  accentColor: '#E74C3C',
  // ...
});
```

### Textes
Tous les textes sont en français et peuvent être modifiés directement dans `App.js`.

## 🚀 Déploiement

### Android
1. Générer un APK de release :
```bash
cd android
./gradlew assembleRelease
```

2. L'APK sera dans : `android/app/build/outputs/apk/release/`

### iOS
1. Ouvrir le projet dans Xcode
2. Configurer les certificats de signature
3. Archiver et distribuer via App Store Connect

## 🔍 Dépannage

### Erreurs courantes
- **Erreur de connexion API** : Vérifiez l'URL de l'API et la connexion internet
- **Erreur de permissions** : Vérifiez les permissions dans AndroidManifest.xml et Info.plist
- **Erreur de build** : Nettoyez le cache : `npx react-native start --reset-cache`

### Logs
```bash
# Android
adb logcat

# iOS
xcrun simctl spawn booted log stream --predicate 'process == "YourApp"'
```

## 📚 Ressources

- [React Native Documentation](https://reactnative.dev/)
- [React Native Image Picker](https://github.com/react-native-image-picker/react-native-image-picker)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 👥 Équipe

**Team RobotMali** - 2025

---

*Application mobile pour la prédiction de minéraux utilisant l'IA.* 