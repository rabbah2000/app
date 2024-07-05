import streamlit as st
import pandas as pd
import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('clients.db')
c = conn.cursor()

# Créer la table des clients si elle n'existe pas
c.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        Nom TEXT,
        Prénom TEXT,
        Article TEXT,
        PDF BLOB
    )
''')
conn.commit()

def load_data():
    c.execute("SELECT * FROM clients")
    data = c.fetchall()
    return pd.DataFrame(data, columns=['Nom', 'Prénom', 'Article', 'PDF'])

def add_data(nom, prenom, article, pdf_data):
    c.execute("INSERT INTO clients (Nom, Prénom, Article, PDF) VALUES (?, ?, ?, ?)", (nom, prenom, article, pdf_data))
    conn.commit()

# Charger les données
clients_df = load_data()

st.title("Gestion des Clients et du Stock")

# Afficher les données chargées
st.header("Tableau des Clients")
st.dataframe(clients_df)

# Formulaire pour ajouter un client et vérifier le stock
st.header("Ajouter un Client et Vérifier le Stock")

with st.form(key='add_client'):
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    article = st.text_input("Article")
    pdf = st.file_uploader("Télécharger un fichier PDF", type=["pdf"])
    submit_button = st.form_submit_button(label='Ajouter et Vérifier le Stock')

    if submit_button:
        pdf_data = pdf.getvalue() if pdf is not None else None
        add_data(nom, prenom, article, pdf_data)
        st.success("Client ajouté avec succès !")

# Afficher les données mises à jour
st.header("Tableau des Clients mis à jour")
clients_df = load_data()
st.dataframe(clients_df)
