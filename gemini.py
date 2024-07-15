import streamlit as st
from google.cloud import gemini
import io

def detect_monument(image_content):
    client = gemini.GeminiClient()

    image = gemini.Image(content=image_content)
    response = client.analyze_image(image=image, features=[{'type': 'LABEL_DETECTION'}])
    labels = response.label_annotations

    return labels

def main():
    st.title("Monument Detection with Google Gemini API")
    
    uploaded_file = st.file_uploader("Choose an image...", type="jpg")

    if uploaded_file is not None:
        image_content = uploaded_file.read()
        
        st.image(image_content, caption='Uploaded Image.', use_column_width=True)
        st.write("")
        st.write("Classifying...")

        labels = detect_monument(image_content)

        st.write("Labels detected:")
        for label in labels:
            st.write(f"- {label.description}")

if __name__ == "__main__":
    main()
