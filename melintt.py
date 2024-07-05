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
        PDF1 BLOB,
        PDF2 BLOB
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

def add_client(ref, compte, affaire, marque, sn_or_mac, date_reception_sav, bon_entree_erm, motif, besoin_piece_importee, date_sortie_sav, suivi_spare_part, bon_sortie_erm, statut, commentaire, pdf_data1):
    c.execute("INSERT INTO clients (REF, Compte, Affaire, Marque, SN_or_MAC, Date_Reception_Sav, Bon_entree_ERM, Motif, Besoin_piece_importee, Date_sortie_sav, Suivi_Spare_Part, Bon_sortie_ERM, Statut, Commentaire, PDF1) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ref, compte, affaire, marque, sn_or_mac, date_reception_sav, bon_entree_erm, motif, besoin_piece_importee, date_sortie_sav, suivi_spare_part, bon_sortie_erm, statut, commentaire, pdf_data1))
    conn.commit()

def add_second_pdf(client_id, pdf_data2):
    c.execute("UPDATE clients SET PDF2 = ? WHERE id = ?", (pdf_data2, client_id))
    conn.commit()

def get_client_pdf(client_id, pdf_number):
    c.execute(f"SELECT PDF{pdf_number} FROM clients WHERE id = ?", (client_id,))
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

def subtract_stock(id, quantity):
    c.execute("SELECT Stock_quantity FROM stock WHERE id = ?", (id,))
    current_quantity = c.fetchone()[0]
    new_quantity = current_quantity - quantity
    if new_quantity < 0:
        new_quantity = 0
    update_stock(id, new_quantity)

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
        pdf1 = st.file_uploader("Télécharger un fichier PDF", type=["pdf"])
        submit_button = st.form_submit_button(label='Ajouter')

        if submit_button:
            pdf_data1 = pdf1.read() if pdf1 is not None else None
            add_client(ref, compte, affaire, marque, sn_or_mac, date_reception_sav, bon_entree_erm, motif, besoin_piece_importee, date_sortie_sav, suivi_spare_part, bon_sortie_erm, statut, commentaire, pdf_data1)
            st.success("Client ajouté avec succès !")

    st.header("Tableau des Clients")
    clients_df = load_clients()
    st.dataframe(clients_df)

    st.header("Ajouter un deuxième PDF à un client existant")
    client_id = st.selectbox("Sélectionnez un client", clients_df["ID"].values)
    pdf2 = st.file_uploader("Télécharger le deuxième fichier PDF", type=["pdf"])
    add_pdf_button = st.button("Ajouter le deuxième PDF")

    if add_pdf_button:
        pdf_data2 = pdf2.read() if pdf2 is not None else None
        add_second_pdf(client_id, pdf_data2)
        st.success("Deuxième PDF ajouté avec succès !")

    st.header("Télécharger un PDF stocké")
    client_id = st.number_input("ID du Client pour téléchargement", min_value=1, step=1)
    pdf_number = st.selectbox("Sélectionnez le PDF à télécharger", [1, 2])
    download_button = st.button("Télécharger le PDF")

    if download_button:
        pdf_data = get_client_pdf(client_id, pdf_number)
        if pdf_data:
            st.download_button(
                label="Télécharger le PDF",
                data=pdf_data,
                file_name=f'client_{client_id}_pdf{pdf_number}.pdf',
                mime='application/pdf'
            )
        else:
            st.error(f"Aucun PDF{pdf_number} trouvé pour cet ID de client.")

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
    stock_id = st.selectbox("Sélectionnez un produit", stock_df["ID"].values)
    selected_stock = stock_df[stock_df["ID"] == stock_id]
    st.write("Part Number:", selected_stock["Part_number"].values[0])
    st.write("Description:", selected_stock["Description"].values[0])
    current_quantity = selected_stock["Stock_quantity"].values[0]
    st.write("Quantité actuelle en stock:", current_quantity)
    subtract_quantity = st.number_input("Quantité à soustraire", min_value=0, max_value=current_quantity, step=1)
    update_button = st.button("Soustraire du Stock")

    if update_button:
        subtract_stock(stock_id, subtract_quantity)
        st.success("Quantité en stock mise à jour avec succès !")
        stock_df = load_stock()
        st.dataframe(stock_df)

# Fermer la connexion à la base de données
conn.close()
