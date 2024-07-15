import streamlit as st
import pathlib
from genai import GenerativeModel
from google.oauth2 import service_account

# Fonction pour générer du contenu en utilisant le modèle génératif
def generate_content_with_model(image_content, prompt):
    # Charger les informations d'identification à partir des secrets
    api_key = st.secrets["api_key"]

    # Initialiser le modèle génératif
    model = GenerativeModel('gemini-1.5-flash', api_key=api_key)

    # Créer la structure de l'image à partir du contenu
    cookie_picture = {
        'mime_type': 'image/png',
        'data': image_content
    }

    # Générer le contenu avec le modèle
    response = model.generate_content(
        contents=[prompt, cookie_picture]
    )
    return response.text

# Fonction principale de l'application Streamlit
def main():
    st.title("Détection de Monuments avec le Modèle Génératif Gemini")
    
    uploaded_file = st.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image_content = uploaded_file.read()
        prompt = st.text_input("Entrez une invite pour l'analyse :", "Do these look store-bought or homemade?")

        st.image(image_content, caption='Image Téléchargée.', use_column_width=True)
        st.write("")
        st.write("Analyse en cours...")

        result = generate_content_with_model(image_content, prompt)

        st.write("Résultat de l'analyse :")
        st.write(result)

if __name__ == "__main__":
    main()
