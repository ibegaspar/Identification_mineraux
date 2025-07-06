import React, { useState } from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  Image,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { launchCamera, launchImageLibrary } from 'react-native-image-picker';

const API_BASE_URL = 'https://votre-api-deployee.com'; // À remplacer par votre URL

const App = () => {
  const [durete, setDurete] = useState('');
  const [densite, setDensite] = useState('');
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const takePhoto = () => {
    const options = {
      mediaType: 'photo',
      quality: 0.8,
      maxWidth: 800,
      maxHeight: 800,
    };

    launchCamera(options, (response) => {
      if (response.didCancel) {
        console.log('Utilisateur a annulé la prise de photo');
      } else if (response.error) {
        Alert.alert('Erreur', 'Erreur lors de la prise de photo');
      } else {
        setImage(response.assets[0]);
      }
    });
  };

  const pickImage = () => {
    const options = {
      mediaType: 'photo',
      quality: 0.8,
      maxWidth: 800,
      maxHeight: 800,
    };

    launchImageLibrary(options, (response) => {
      if (response.didCancel) {
        console.log('Utilisateur a annulé la sélection');
      } else if (response.error) {
        Alert.alert('Erreur', 'Erreur lors de la sélection d\'image');
      } else {
        setImage(response.assets[0]);
      }
    });
  };

  const predictMineral = async () => {
    if (!durete || !densite) {
      Alert.alert('Erreur', 'Veuillez remplir la dureté et la densité');
      return;
    }

    if (parseFloat(durete) < 0 || parseFloat(durete) > 10) {
      Alert.alert('Erreur', 'La dureté doit être entre 0 et 10');
      return;
    }

    if (parseFloat(densite) < 0 || parseFloat(densite) > 20) {
      Alert.alert('Erreur', 'La densité doit être entre 0 et 20');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const formData = new FormData();
      
      if (image) {
        // Prédiction avec image
        formData.append('image', {
          uri: image.uri,
          type: image.type || 'image/jpeg',
          name: image.fileName || 'mineral.jpg',
        });
        formData.append('durete', durete);
        formData.append('densite', densite);

        const response = await fetch(`${API_BASE_URL}/predict`, {
          method: 'POST',
          body: formData,
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        const data = await response.json();
        
        if (response.ok) {
          setResult(data);
        } else {
          Alert.alert('Erreur', data.detail || 'Erreur lors de la prédiction');
        }
      } else {
        // Prédiction simple sans image
        formData.append('durete', durete);
        formData.append('densite', densite);

        const response = await fetch(`${API_BASE_URL}/predict_simple`, {
          method: 'POST',
          body: formData,
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        const data = await response.json();
        
        if (response.ok) {
          setResult(data);
        } else {
          Alert.alert('Erreur', data.detail || 'Erreur lors de la prédiction');
        }
      }
    } catch (error) {
      console.error('Erreur:', error);
      Alert.alert('Erreur', 'Erreur de connexion à l\'API');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setDurete('');
    setDensite('');
    setImage(null);
    setResult(null);
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor="#f8f9fa" />
      
      <ScrollView contentContainerStyle={styles.scrollView}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>🔬 Prédiction Minéraux</Text>
          <Text style={styles.subtitle}>Team RobotMali</Text>
        </View>

        {/* Image Section */}
        <View style={styles.imageSection}>
          <Text style={styles.sectionTitle}>📸 Image du minéral</Text>
          
          <View style={styles.imageButtons}>
            <TouchableOpacity style={styles.imageButton} onPress={takePhoto}>
              <Text style={styles.buttonText}>📷 Prendre une photo</Text>
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.imageButton} onPress={pickImage}>
              <Text style={styles.buttonText}>🖼️ Choisir une image</Text>
            </TouchableOpacity>
          </View>

          {image && (
            <View style={styles.imagePreview}>
              <Image source={{ uri: image.uri }} style={styles.previewImage} />
              <Text style={styles.imageInfo}>Image sélectionnée</Text>
            </View>
          )}
        </View>

        {/* Form Section */}
        <View style={styles.formSection}>
          <Text style={styles.sectionTitle}>📋 Propriétés physiques</Text>
          
          <View style={styles.inputContainer}>
            <Text style={styles.label}>Dureté (échelle de Mohs)</Text>
            <TextInput
              style={styles.input}
              value={durete}
              onChangeText={setDurete}
              placeholder="Ex: 7.0"
              keyboardType="numeric"
              maxLength={4}
            />
            <Text style={styles.hint}>Valeur entre 0 et 10</Text>
          </View>

          <View style={styles.inputContainer}>
            <Text style={styles.label}>Densité (g/cm³)</Text>
            <TextInput
              style={styles.input}
              value={densite}
              onChangeText={setDensite}
              placeholder="Ex: 3.5"
              keyboardType="numeric"
              maxLength={5}
            />
            <Text style={styles.hint}>Valeur entre 0 et 20</Text>
          </View>
        </View>

        {/* Action Buttons */}
        <View style={styles.actionSection}>
          <TouchableOpacity
            style={[styles.predictButton, loading && styles.disabledButton]}
            onPress={predictMineral}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.predictButtonText}>🔍 Prédire le minéral</Text>
            )}
          </TouchableOpacity>

          <TouchableOpacity style={styles.resetButton} onPress={resetForm}>
            <Text style={styles.resetButtonText}>🔄 Réinitialiser</Text>
          </TouchableOpacity>
        </View>

        {/* Result Section */}
        {result && (
          <View style={styles.resultSection}>
            <Text style={styles.sectionTitle}>🎯 Résultat</Text>
            
            <View style={styles.resultCard}>
              <Text style={styles.resultMineral}>
                {result.predicted_mineral}
              </Text>
              <Text style={styles.resultConfidence}>
                Confiance: {result.confidence.toFixed(1)}%
              </Text>
              
              {result.method && (
                <Text style={styles.resultMethod}>
                  Méthode: {result.method === 'physical_properties_only' ? 'Propriétés physiques uniquement' : 'IA complète'}
                </Text>
              )}
            </View>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  scrollView: {
    padding: 20,
  },
  header: {
    alignItems: 'center',
    marginBottom: 30,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#2C3E50',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 16,
    color: '#7F8C8D',
  },
  imageSection: {
    marginBottom: 30,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#34495E',
    marginBottom: 15,
  },
  imageButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  imageButton: {
    flex: 1,
    backgroundColor: '#3498DB',
    padding: 15,
    borderRadius: 10,
    marginHorizontal: 5,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  imagePreview: {
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: '#E8F4FD',
  },
  previewImage: {
    width: 200,
    height: 200,
    borderRadius: 10,
    marginBottom: 10,
  },
  imageInfo: {
    color: '#27AE60',
    fontWeight: 'bold',
  },
  formSection: {
    marginBottom: 30,
  },
  inputContainer: {
    marginBottom: 20,
  },
  label: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2C3E50',
    marginBottom: 8,
  },
  input: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#BDC3C7',
    borderRadius: 8,
    padding: 15,
    fontSize: 16,
  },
  hint: {
    fontSize: 12,
    color: '#7F8C8D',
    marginTop: 5,
  },
  actionSection: {
    marginBottom: 30,
  },
  predictButton: {
    backgroundColor: '#27AE60',
    padding: 18,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 15,
  },
  disabledButton: {
    backgroundColor: '#95A5A6',
  },
  predictButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 18,
  },
  resetButton: {
    backgroundColor: '#E74C3C',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  resetButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  resultSection: {
    marginBottom: 30,
  },
  resultCard: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 15,
    borderWidth: 2,
    borderColor: '#E8F4FD',
    alignItems: 'center',
  },
  resultMineral: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#E74C3C',
    marginBottom: 10,
  },
  resultConfidence: {
    fontSize: 18,
    color: '#27AE60',
    fontWeight: 'bold',
    marginBottom: 5,
  },
  resultMethod: {
    fontSize: 14,
    color: '#7F8C8D',
    fontStyle: 'italic',
  },
});

export default App; 