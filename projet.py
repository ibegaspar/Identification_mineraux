import streamlit as st
import numpy as np
import pandas as pd
import cv2
import keras
import joblib
import os

# === Vérification stricte des fichiers ===
REQUIRED_FILES = [
    'model_final_durete_densiter.h5',
    'scaler.pkl',
    'label_encoder.pkl'
]
missing_files = [f for f in REQUIRED_FILES if not os.path.exists(f)]
if missing_files:
    st.error(f"❌ Fichiers manquants : {', '.join(missing_files)}. Placez-les dans le dossier du projet.")
    st.stop()

# === Chargement strict des objets ===
model = None
scaler = None
label_encoder = None

try:
    model = keras.models.load_model('model_final_durete_densiter.h5')
except Exception as e:
    st.error(f"❌ Erreur lors du chargement du modèle : {e}")
    st.stop()

try:
    scaler = joblib.load('scaler.pkl')
except Exception as e:
    st.error(f"❌ Erreur lors du chargement du scaler : {e}")
    st.stop()

try:
    label_encoder = joblib.load('label_encoder.pkl')
except Exception as e:
    st.error(f"❌ Erreur lors du chargement du label encoder : {e}")
    st.stop()

IMG_SIZE = (380, 380)

def preprocess_image_bytes(bytes_data):
    nparr = np.frombuffer(bytes_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.resize(img, IMG_SIZE)
    img = img.astype(np.float32) / 255.0
    return img

# === Interface utilisateur ===
st.markdown(
    """
    <h1 style='text-align: center; color: #2C3E50;'>Prédiction de Minéral</h1>
    <p style='text-align: center; color: #34495E;'>Prenez une photo ou importez une image, saisissez la dureté et la densité, puis obtenez la prédiction du minéral.</p>
    <hr>
    """, unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    img_buffer = st.camera_input("Prendre une photo")
    st.markdown("<div style='text-align:center;'>ou</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Importer une image", type=["jpg", "jpeg", "png"])
    if img_buffer is not None:
        st.success("📸 Photo reçue !")
    elif uploaded_file is not None:
        st.success("🖼️ Image importée !")

with col2:
    st.subheader("📋 Formulaire d'analyse")
    durete = st.number_input("Dureté", min_value=0.0, max_value=20.0, step=0.1, help="Dureté du minéral (échelle de Mohs)")
    densite = st.number_input("Densité", min_value=0.0, max_value=20.0, step=0.01, help="Densité du minéral (g/cm³)")
    submit = st.button("🔍 Prédire le minéral", type="primary", disabled=(img_buffer is None and uploaded_file is None))

# On choisit l'image à traiter : priorité à l'image uploadée
image_source = uploaded_file if uploaded_file is not None else img_buffer

if image_source is not None and submit:
    try:
        with st.spinner("🔄 Traitement en cours..."):
            # Prétraitement image
            img = preprocess_image_bytes(image_source.getvalue())
            X_img = np.expand_dims(img, axis=0)
            # Prétraitement tabulaire
            X_tab = scaler.transform([[durete, densite]])
            # Prédiction
            if model is not None:
                prediction = model.predict([X_img, X_tab], verbose=0)
                predicted_index = np.argmax(prediction)
                predicted_mineral = label_encoder.inverse_transform([predicted_index])[0]
            else:
                st.error("❌ Modèle non chargé")
                st.stop()
        # Affichage du résultat
        st.markdown("---")
        st.markdown(
            f"""
            <div style='text-align: center; padding: 20px; background-color: #f0f8ff; border-radius: 10px;'>
                <h2 style='color: #27AE60;'>🎯 Résultat de la prédiction</h2>
                <h3 style='color: #2C3E50;'>Minéral prédit : <span style='color: #E74C3C; font-weight: bold;'>{predicted_mineral}</span></h3>
                <p style='color: #7F8C8D;'>Confiance : {np.max(prediction[0])*100:.1f}%</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        # Affichage de l'image traitée
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.image(image_source, caption="Image originale")
        with col_img2:
            st.image(img, caption="🖼️ Image traitée", clamp=True)
    except Exception as e:
        st.error(f"❌ Erreur lors de la prédiction: {e}")

# Footer
st.markdown(
    """
    <hr>
    <div style='text-align: center; color: #95A5A6; padding: 20px;'>
        <p>🔬 Application de prédiction de minéraux</p>
        <p>copyright@ 2025 by Team RobotMali</p>
    </div>
    """,
    unsafe_allow_html=True
)
