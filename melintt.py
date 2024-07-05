import streamlit as st
import pandas as pd
import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Créer les tables si elles n'existent pas
c.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        REF TEXT,
        Compte TEXT,
        Affaire TEXT,
        Marque TEXT,
        SN_or_MAC TEXT,
        Date_Reception_Sav TEXT,
        Bon_entree_ERM TEXT,
        Motif TEXT,
        Besoin_piece_importee TEXT,
        Date_sortie_sav TEXT,
        Suivi_Spare_Part TEXT,
        Bon_sortie_ERM TEXT,
        Statut TEXT,
        Commentaire TEXT,
        PDF BLOB
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Part_number TEXT,
        Description TEXT,
        Stock_quantity INTEGER
    )
''')
conn.commit()

### Fonctions pour la table clients

def load_clients():
    c.execute("SELECT id, REF, Compte, Affaire, Marque, SN_or_MAC, Date_Reception_Sav, Bon_entree_ERM, Motif, Besoin_piece_importee, Date_sortie_sav, Suivi_Spare_Part, Bon_sortie_ERM, Statut, Commentaire FROM clients")
    data = c.fetchall()
    return pd.DataFrame(data, columns=['ID', 'REF', 'Compte', 'Affaire', 'Marque', 'SN_or_MAC', 'Date_Reception_Sav', 'Bon_entree_ERM', 'Motif', 'Besoin_piece_importee', 'Date_sortie_sav', 'Suivi_Spare_Part', 'Bon_sortie_ERM', 'Statut', 'Commentaire'])

def add_client(ref, compte, affaire, marque, sn_or_mac, date_reception_sav, bon_entree_erm, motif, besoin_piece_importee, date_sortie_sav, suivi_spare_part, bon_sortie_erm, statut, commentaire, pdf_data):
    c.execute("INSERT INTO clients (REF, Compte, Affaire, Marque, SN_or_MAC, Date_Reception_Sav, Bon_entree_ERM, Motif, Besoin_piece_importee, Date_sortie_sav, Suivi_Spare_Part, Bon_sortie_ERM, Statut, Commentaire, PDF) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ref, compte, affaire, marque, sn_or_mac, date_reception_sav, bon_entree_erm, motif, besoin_piece_importee, date_sortie_sav, suivi_spare_part, bon_sortie_erm, statut, commentaire, pdf_data))
    conn.commit()

def get_client_pdf(id):
    c.execute("SELECT PDF FROM clients WHERE id = ?", (id,))
    pdf_data = c.fetchone()[0]
    return pdf_data

### Fonctions pour la table stock

def load_stock():
    c.execute("SELECT id, Part_number, Description, Stock_quantity FROM stock")
    data = c.fetchall()
    return pd.DataFrame(data, columns=['ID', 'Part_number', 'Description', 'Stock_quantity'])

def add_stock(part_number, description, stock_quantity):
    c.execute("INSERT INTO stock (Part_number, Description, Stock_quantity) VALUES (?, ?, ?)", (part_number, description, stock_quantity))
    conn.commit()

def update_stock(id, stock_quantity):
    c.execute("UPDATE stock SET Stock_quantity = ? WHERE id = ?", (stock_quantity, id))
    conn.commit()

# Interface Streamlit
st.title("Gestion des Clients et du Stock")

# Sélectionner la table à afficher/ajouter des données
table_selection = st.selectbox("Sélectionnez la table", ["Clients", "Stock"])

if table_selection == "Clients":
    st.header("Ajouter un Client et Télécharger un PDF")
    with st.form(key='add_client'):
        ref = st.text_input("REF")
        compte = st.text_input("Compte")
        affaire = st.text_input("Affaire")
        marque = st.text_input("Marque")
        sn_or_mac = st.text_input("S/N ou MAC")
        date_reception_sav = st.text_input("Date Reception Sav")
        bon_entree_erm = st.text_input("Bon d'entree ERM")
        motif = st.text_input("Motif")
        besoin_piece_importee = st.text_input("Besoin de piece importee")
        date_sortie_sav = st.text_input("Date de sortie sav")
        suivi_spare_part = st.text_input("SUIVI SPARE PART")
        bon_sortie_erm = st.text_input("Bon de sortie ERM")
        statut = st.text_input("Statut")
        commentaire = st.text_area("Commentaire")
        pdf = st.file_uploader("Télécharger un fichier PDF", type=["pdf"])
        submit_button = st.form_submit_button(label='Ajouter')

        if submit_button:
            pdf_data = pdf.read() if pdf is not None else None
            add_client(ref, compte, affaire, marque, sn_or_mac, date_reception_sav, bon_entree_erm, motif, besoin_piece_importee, date_sortie_sav, suivi_spare_part, bon_sortie_erm, statut, commentaire, pdf_data)
            st.success("Client ajouté avec succès !")

    st.header("Tableau des Clients")
    clients_df = load_clients()
    st.dataframe(clients_df)

    st.header("Télécharger un PDF stocké")
    client_id = st.number_input("ID du Client", min_value=1, step=1)
    download_button = st.button("Télécharger le PDF")

    if download_button:
        pdf_data = get_client_pdf(client_id)
        if pdf_data:
            st.download_button(
                label="Télécharger le PDF",
                data=pdf_data,
                file_name=f'client_{client_id}.pdf',
                mime='application/pdf'
            )
        else:
            st.error("Aucun PDF trouvé pour cet ID de client.")

elif table_selection == "Stock":
    st.header("Ajouter un Produit au Stock")
    with st.form(key='add_stock'):
        part_number = st.text_input("Part Number")
        description = st.text_input("Description")
        stock_quantity = st.number_input("Stock Quantity", min_value=0, step=1)
        submit_button = st.form_submit_button(label='Ajouter')

        if submit_button:
            add_stock(part_number, description, stock_quantity)
            st.success("Produit ajouté au stock avec succès !")

    st.header("Tableau du Stock")
    stock_df = load_stock()
    st.dataframe(stock_df)

    st.header("Modifier la Quantité en Stock")
    stock_id = st.number_input("ID du Produit", min_value=1, step=1)
    new_stock_quantity = st.number_input("Nouvelle Quantité en Stock", min_value=0, step=1)
    update_button = st.button("Mettre à Jour le Stock")

    if update_button:
        update_stock(stock_id, new_stock_quantity)
        st.success("Quantité en stock mise à jour avec succès !")
        stock_df = load_stock()
        st.dataframe(stock_df)

# Fermer la connexion à la base de données
conn.close()
