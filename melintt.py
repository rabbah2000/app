import streamlit as st
import pandas as pd
import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('clients.db')
c = conn.cursor()

# Créer la table des clients si elle n'existe pas
c.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom TEXT,
        Prénom TEXT,
        Article TEXT,
        PDF BLOB
    )
''')
conn.commit()

def load_data():
    c.execute("SELECT id, Nom, Prénom, Article FROM clients")
    data = c.fetchall()
    return pd.DataFrame(data, columns=['ID', 'Nom', 'Prénom', 'Article'])

def add_data(nom, prenom, article, pdf_data):
    c.execute("INSERT INTO clients (Nom, Prénom, Article, PDF) VALUES (?, ?, ?, ?)", (nom, prenom, article, pdf_data))
    conn.commit()

def get_pdf(id):
    c.execute("SELECT PDF FROM clients WHERE id = ?", (id,))
    pdf_data = c.fetchone()[0]
    return pdf_data

# Interface Streamlit
st.title("Gestion des Clients et du Stock")

# Formulaire pour ajouter un client et un PDF
st.header("Ajouter un Client et Télécharger un PDF")

with st.form(key='add_client'):
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    article = st.text_input("Article")
    pdf = st.file_uploader("Télécharger un fichier PDF", type=["pdf"])
    submit_button = st.form_submit_button(label='Ajouter')

    if submit_button:
        pdf_data = pdf.read() if pdf is not None else None
        add_data(nom, prenom, article, pdf_data)
        st.success("Client ajouté avec succès !")

# Afficher les données mises à jour
st.header("Tableau des Clients")
clients_df = load_data()
st.dataframe(clients_df)

# Télécharger un PDF stocké
st.header("Télécharger un PDF stocké")
client_id = st.number_input("ID du Client", min_value=1, step=1)
download_button = st.button("Télécharger le PDF")

if download_button:
    pdf_data = get_pdf(client_id)
    if pdf_data:
        st.download_button(
            label="Télécharger le PDF",
            data=pdf_data,
            file_name=f'client_{client_id}.pdf',
            mime='application/pdf'
        )
    else:
        st.error("Aucun PDF trouvé pour cet ID de client.")
