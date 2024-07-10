import streamlit as st

# CSS pour styliser le portfolio
st.markdown("""
    <style>
        .main-title {
            font-size: 36px;
            font-weight: bold;
            color: #2E86C1;
            text-align: center;
            margin-bottom: 20px;
        }
        .subheader {
            font-size: 24px;
            color: #2874A6;
            text-align: center;
            margin-bottom: 40px;
        }
        .section-title {
            font-size: 28px;
            font-weight: bold;
            color: #1B4F72;
            margin-top: 40px;
            margin-bottom: 20px;
        }
        .section-content {
            font-size: 18px;
            color: #515A5A;
            margin-bottom: 20px;
        }
        .contact-info {
            font-size: 18px;
            color: #515A5A;
            text-align: center;
            margin-bottom: 40px;
        }
    </style>
""", unsafe_allow_html=True)

# Accueil
st.markdown('<div class="main-title">Rabbah Imrane</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Élève Ingénieur en Génie de la Data</div>', unsafe_allow_html=True)
st.markdown('<div class="contact-info">+212 708-258298 | RABAT, Agdal | rabbahimrane6@gmail.com</div>', unsafe_allow_html=True)

# À propos de moi
st.markdown('<div class="section-title">À propos de moi</div>', unsafe_allow_html=True)
st.markdown('<div class="section-content">Je suis un étudiant en première année à l’ENSIAS, spécialisé en ingénierie de la data. Passionné par l’analyse des données et le développement de solutions informatiques innovantes, je cherche à rejoindre une équipe dynamique où je pourrai contribuer avec mes compétences techniques et mon esprit d’équipe.</div>', unsafe_allow_html=True)

# Compétences
st.markdown('<div class="section-title">Compétences</div>', unsafe_allow_html=True)
st.markdown('<div class="section-content">', unsafe_allow_html=True)
st.markdown('- **Programmation** : Python (Flask, Streamlit), SQL, PLSQL, Java (programmation orientée objet)', unsafe_allow_html=True)
st.markdown('- **Machine Learning et Traitement de données** : traitement d’image, traitement d’audio', unsafe_allow_html=True)
st.markdown('- **Systèmes d’exploitation** : Linux, Windows', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Expériences
st.markdown('<div class="section-title">Expériences</div>', unsafe_allow_html=True)
st.markdown('<div class="section-content">', unsafe_allow_html=True)
st.markdown('**Responsable data, AI CLUB RABAT, ENSIAS (2023)**', unsafe_allow_html=True)
st.markdown('• Supervision des projets de data science et analyse des données pour divers cas d’étude.', unsafe_allow_html=True)
st.markdown('**Vice Team Leader, Enactus ENSIAS (2023)**', unsafe_allow_html=True)
st.markdown('• Gestion d’une équipe de 5 membres pour développer des projets à impact social et innovant.', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Projets
st.markdown('<div class="section-title">Projets</div>', unsafe_allow_html=True)
st.markdown('<div class="section-content">', unsafe_allow_html=True)
st.markdown('**E-Service**', unsafe_allow_html=True)
st.markdown('• Développement d’une application e-service avec analyse prédictive des besoins des utilisateurs. Mise en place de fonctionnalités prédictives pour anticiper les besoins des utilisateurs basées sur l’historique et les tendances de données. Utilisation d’algorithmes de machine learning pour personnaliser les recommandations de services.', unsafe_allow_html=True)
st.markdown('**Train**', unsafe_allow_html=True)
st.markdown('• Conception et développement d’une base de données en SQL pour gérer les voyages en train.', unsafe_allow_html=True)
st.markdown('**Chatbot**', unsafe_allow_html=True)
st.markdown('• Conception et développement d’un chatbot capable d’analyser le contenu de fichiers PDF pour fournir des réponses contextuelles.', unsafe_allow_html=True)
st.markdown('**Securway**', unsafe_allow_html=True)
st.markdown('• Participation au projet Securway, axé sur la prévention de la somnolence des conducteurs.', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Éducation
st.markdown('<div class="section-title">Éducation</div>', unsafe_allow_html=True)
st.markdown('<div class="section-content">', unsafe_allow_html=True)
st.markdown('**Élève Ingénieur 1ère année en Génie Informatique, L’Ecole Nationale Supérieure d’informatique et d’Analyse des Systèmes (ENSIAS) (2023)**', unsafe_allow_html=True)
st.markdown('**Classes préparatoires, Lycée technique Mohammedia (2021-2023)**', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Langues
st.markdown('<div class="section-title">Langues</div>', unsafe_allow_html=True)
st.markdown('<div class="section-content">', unsafe_allow_html=True)
st.markdown('**Anglais** : Conversational', unsafe_allow_html=True)
st.markdown('**Français** : Niveau professionnel', unsafe_allow_html=True)
st.markdown('**Arabe** : Langue maternelle', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Centres d'intérêt
st.markdown('<div class="section-title">Centres d\'intérêt</div>', unsafe_allow_html=True)
st.markdown('<div class="section-content">', unsafe_allow_html=True)
st.markdown('- Analyse de données', unsafe_allow_html=True)
st.markdown('- Systèmes de gestion de base de données', unsafe_allow_html=True)
st.markdown('- Machine learning', unsafe_allow_html=True)
st.markdown('- Nettoyage des données', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
