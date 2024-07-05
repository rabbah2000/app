import streamlit as st
import pandas as pd
import sqlite3

# Identifiants pré-définis
users = {"admin": "adminpass", "user1": "password1", "user2": "password2"}

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
        Produit TEXT,
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
    c.execute("SELECT id, REF, Compte, Affaire, Marque, SN_or_MAC, Date_Reception_Sav, Bon_entree_ERM, Motif, Besoin_piece_importee, Date_sortie_sav, Suivi_Spare_Part, Bon_sortie_ERM, Statut, Commentaire, Produit FROM clients")
    data = c.fetchall()
    return pd.DataFrame(data, columns=['ID', 'REF', 'Compte', 'Affaire', 'Marque', 'SN_or_MAC', 'Date_Reception_Sav', 'Bon_entree_ERM', 'Motif', 'Besoin_piece_importee', 'Date_sortie_sav', 'Suivi_Spare_Part', 'Bon_sortie_ERM', 'Statut', 'Commentaire', 'Produit'])

def add_client(ref, compte, affaire, marque, sn_or_mac, date_reception_sav, bon_entree_erm, motif, besoin_piece_importee, date_sortie_sav, suivi_spare_part, bon_sortie_erm, statut, commentaire, produit, pdf_data1):
    c.execute("INSERT INTO clients (REF, Compte, Affaire, Marque, SN_or_MAC, Date_Reception_Sav, Bon_entree_ERM, Motif, Besoin_piece_importee, Date_sortie_sav, Suivi_Spare_Part, Bon_sortie_ERM, Statut, Commentaire, Produit, PDF1) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ref, compte, affaire, marque, sn_or_mac, date_reception_sav, bon_entree_erm, motif, besoin_piece_importee, date_sortie_sav, suivi_spare_part, bon_sortie_erm, statut, commentaire, produit, pdf_data1))
    conn.commit()
    if produit:
        subtract_stock(produit, 1)  # Soustraire une unité du stock

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

def subtract_stock(part_number, quantity):
    c.execute("SELECT Stock_quantity FROM stock WHERE Part_number = ?", (part_number,))
    current_quantity = c.fetchone()[0]
    new_quantity = current_quantity - quantity
    if new_quantity < 0:
        new_quantity = 0
    c.execute("UPDATE stock SET Stock_quantity = ? WHERE Part_number = ?", (new_quantity, part_number))
    conn.commit()

# Interface Streamlit

# Fonction d'authentification
def authenticate(username, password):
    if username in users and users[username] == password:
        return True
    return False

# Page de login
def login():
    st.title("Login")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    login_button = st.button("Se connecter")
    
    if login_button:
        if authenticate(username, password):
            st.session_state["authenticated"] = True
            st.experimental_rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")

# Page principale après authentification
def main_page():
    st.title("Gestion Melint SAV")

    # Ajouter un logo en haut de la page et définir le fond blanc
    st.markdown(
        """
        <style>
            .reportview-container {
                background-color: white;
            }
            .sidebar .sidebar-content {
                background-color: white;
            }
            .reportview-container .main .block-container {
                padding-top: 2rem;
            }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        <div style="display: flex; justify-content: center; align-items: center; padding-bottom: 2rem;">
            <img src="https://static.wixstatic.com/media/f3d32c_c3a12fb4cf6642419034f4a981afd6f8~mv2.jpg/v1/fill/w_185,h_233,al_c,q_80,usm_0.66_1.00_0.01,enc_auto/f3d32c_c3a12fb4cf6642419034f4a981afd6f8~mv2.jpg" alt="Logo" width="200">
        </div>
        """,
        unsafe_allow_html=True
    )

    # Ajouter le favicon


    # Sélectionner la table à afficher/ajouter des données
    table_selection = st.selectbox("Sélectionnez la table", ["Tableau des articles SAV", "Tableau des piéces de rechange"])

    if table_selection == "Tableau des articles SAV":
        st.header("Ajouter un article SAV")
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
            stock_df = load_stock()
            part_number = st.selectbox("Sélectionnez le numéro de pièce (ou laissez vide)", [""] + stock_df["Part_number"].tolist())
            pdf1 = st.file_uploader("Télécharger formulaire clinet", type=["pdf"])
            submit_button = st.form_submit_button(label='Ajouter')

            if submit_button:
                pdf_data1 = pdf1.read() if pdf1 is not None else None
                add_client(ref, compte, affaire, marque, sn_or_mac, date_reception_sav, bon_entree_erm, motif, besoin_piece_importee, date_sortie_sav, suivi_spare_part, bon_sortie_erm, statut, commentaire, part_number, pdf_data1)
                st.success("Client ajouté avec succès et stock mis à jour !")

        st.header("Inventaire de piéces de rechange")
        clients_df = load_clients()
        st.dataframe(clients_df)

        st.header("Ajouter le rapport de diagnostique")
        client_id = st.selectbox("Sélectionnez un client", clients_df["ID"].values)
        pdf2 = st.file_uploader("Télécharger le deuxième fichier PDF", type=["pdf"])
        add_pdf_button = st.button("Ajouter le deuxième PDF")

        if add_pdf_button:
            pdf_data2 = pdf2.read() if pdf2 is not None else None
            add_second_pdf(client_id, pdf_data2)
            st.success("Deuxième PDF ajouté avec succès !")

        st.header("Télécharger la formulaire client et le rapport de diagnostique")
        client_id = st.number_input("ID du Client pour téléchargement", min_value=1, step=1)
        pdf_option = st.selectbox("Sélectionnez le PDF à télécharger", ["la formulaire client", "le rapport de diagnostique"])
        pdf_number = 1 if pdf_option == "la formulaire client" else 2
        download_button = st.button("Télécharger le PDF")

        if download_button:
            pdf_data = get_client_pdf(client_id, pdf_number)
            if pdf_data:
                st.download_button(
                    label="Télécharger le PDF",
                    data=pdf_data,
                    file_name=f'client_{client_id}_{pdf_option.replace(" ", "_")}.pdf',
                    mime='application/pdf'
                )
            else:
                st.error(f"Aucun {pdf_option} trouvé pour cet ID de client.")

        # Ajouter une section pour charger un fichier Excel
        st.header("Charger les données à partir d'un fichier Excel")
        excel_file = st.file_uploader("Téléchargez le fichier Excel", type=["xlsx"])

        if excel_file:
            df_excel = pd.read_excel(excel_file)
            st.dataframe(df_excel)

    elif table_selection == "Tableau des piéces de rechange":
        st.header("Ajouter un SPART PART")
        with st.form(key='add_stock'):
            part_number = st.text_input("Part Number")
            description = st.text_input("Description")
            stock_quantity = st.number_input("Stock Quantity", min_value=0, step=1)
            submit_button = st.form_submit_button(label='Ajouter')

            if submit_button:
                add_stock(part_number, description, stock_quantity)
                st.success("Produit ajouté au stock avec succès !")

        st.header("Tableau du piéces de rechange")
        stock_df = load_stock()
        st.dataframe(stock_df)

        # Ajouter une section pour charger un fichier Excel
        st.header("Charger les données à partir d'un fichier Excel")
        excel_file = st.file_uploader("Téléchargez le fichier Excel", type=["xlsx"])

        if excel_file:
            df_excel = pd.read_excel(excel_file)
            st.dataframe(df_excel)

# Authentification et accès conditionnel
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
    main_page()
else:
    login()

# Fermer la connexion à la base de données
conn.close()
