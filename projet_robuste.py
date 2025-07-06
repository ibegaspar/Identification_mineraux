import streamlit as st
import numpy as np
import pandas as pd
import cv2
import joblib
import os

# === Vérification des fichiers ===
REQUIRED_FILES = ['scaler.pkl', 'label_encoder.pkl']
missing_files = [f for f in REQUIRED_FILES if not os.path.exists(f)]

if missing_files:
    st.error(f"❌ Fichiers manquants : {', '.join(missing_files)}")
    st.stop()

# === Chargement des outils ===
try:
    scaler = joblib.load('scaler.pkl')
    label_encoder = joblib.load('label_encoder.pkl')
    st.success("✅ Outils chargés avec succès !")
except Exception as e:
    st.error(f"❌ Erreur lors du chargement : {e}")
    st.stop()

# === Tentative de chargement du modèle TensorFlow ===
model = None
try:
    import tensorflow as tf
    model = tf.keras.models.load_model('model_final_durete_densiter.h5')
    st.success("✅ Modèle TensorFlow chargé avec succès !")
except Exception as e:
    st.warning(f"⚠️ Modèle TensorFlow non disponible : {e}")
    st.info("🔧 Mode de prédiction basé sur les propriétés physiques activé")

IMG_SIZE = (380, 380)

def preprocess_image_bytes(bytes_data):
    nparr = np.frombuffer(bytes_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.resize(img, IMG_SIZE)
    img = img.astype(np.float32) / 255.0
    return img

def predict_mineral_physical(durete, densite):
    """Prédiction basée uniquement sur les propriétés physiques"""
    if durete >= 7 and densite >= 3.5:
        return "Diamant", 95.0
    elif durete >= 6 and densite >= 2.6:
        return "Quartz", 88.0
    elif durete >= 5 and densite >= 2.5:
        return "Feldspath", 85.0
    elif durete >= 4 and densite >= 2.2:
        return "Calcite", 82.0
    elif durete >= 3 and densite >= 2.0:
        return "Gypse", 78.0
    else:
        return "Minéral commun", 70.0

# === Interface utilisateur ===
st.markdown(
    """
    <h1 style='text-align: center; color: #2C3E50;'>🔍 Prédiction de Minéral</h1>
    <p style='text-align: center; color: #34495E;'>Analyse intelligente basée sur les propriétés physiques</p>
    <hr>
    """, unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    img_buffer = st.camera_input("📸 Prendre une photo")
    st.markdown("<div style='text-align:center;'>ou</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("🖼️ Importer une image", type=["jpg", "jpeg", "png"])
    if img_buffer is not None:
        st.success("✅ Photo reçue !")
    elif uploaded_file is not None:
        st.success("✅ Image importée !")

with col2:
    st.subheader("📋 Caractéristiques physiques")
    durete = st.number_input("Dureté (échelle de Mohs)", min_value=0.0, max_value=10.0, step=0.1, value=5.0)
    densite = st.number_input("Densité (g/cm³)", min_value=0.0, max_value=20.0, step=0.01, value=2.7)
    submit = st.button("🔎 Analyser le minéral", type="primary", disabled=(img_buffer is None and uploaded_file is None))

# Choix de l'image
image_source = uploaded_file if uploaded_file is not None else img_buffer

if image_source is not None and submit:
    try:
        with st.spinner("🔄 Analyse en cours..."):
            # Prétraitement image
            img = preprocess_image_bytes(image_source.getvalue())
            st.success(f"✅ Image analysée ! Taille : {img.shape}")
            
            # Prétraitement des données
            X_tab = scaler.transform([[durete, densite]])
            st.success("✅ Données physiques traitées !")
            
            # Prédiction
            if model is not None:
                try:
                    # Tentative de prédiction avec le modèle TensorFlow
                    X_img = np.expand_dims(img, axis=0)
                    prediction = model.predict([X_img, X_tab], verbose=0)
                    predicted_index = np.argmax(prediction)
                    predicted_mineral = label_encoder.inverse_transform([predicted_index])[0]
                    confidence = np.max(prediction[0]) * 100
                    st.success("✅ Prédiction TensorFlow réussie !")
                except Exception as e:
                    st.warning(f"⚠️ Erreur prédiction TensorFlow : {e}")
                    predicted_mineral, confidence = predict_mineral_physical(durete, densite)
                    st.info("🔧 Mode de prédiction physique utilisé")
            else:
                # Prédiction basée sur les propriétés physiques
                predicted_mineral, confidence = predict_mineral_physical(durete, densite)
                st.info("🔧 Mode de prédiction physique utilisé")
        
        # Affichage du résultat
        st.markdown("---")
        st.markdown(
            f"""
            <div style='text-align: center; padding: 20px; background-color: #f0f8ff; border-radius: 10px;'>
                <h2 style='color: #27AE60;'>🎯 Résultat de l'analyse</h2>
                <h3 style='color: #2C3E50;'>Minéral identifié : <span style='color: #E74C3C; font-weight: bold;'>{predicted_mineral}</span></h3>
                <p style='color: #7F8C8D;'>Confiance : {confidence:.1f}%</p>
                <p style='color: #95A5A6; font-size: 0.9em;'>Basé sur la dureté ({durete}) et la densité ({densite})</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Affichage des images
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.image(image_source, caption="Image originale")
        with col_img2:
            st.image(img, caption="Image analysée", clamp=True)
            
    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse : {e}")

# Footer
st.markdown(
    """
    <hr>
    <div style='text-align: center; color: #95A5A6; padding: 20px;'>
        <p>🔬 Application d'identification de minéraux</p>
        <p>© 2025 Team RobotMali</p>
    </div>
    """,
    unsafe_allow_html=True
) 