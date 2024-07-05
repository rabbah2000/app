import streamlit as st
import pandas as pd

# Empty data for clients and example data for stock
clients_data = {
    'Nom': [],
    'Prénom': [],
    'Article': [],
    'PDF': []
}

stock_data = {
    'Article': ['Laptop', 'Mouse', 'Keyboard', 'Monitor'],
    'Quantité': [10, 50, 30, 20]
}

# Initialize session state for dataframes
if 'clients_df' not in st.session_state:
    st.session_state.clients_df = pd.DataFrame(clients_data)
if 'stock_df' not in st.session_state:
    st.session_state.stock_df = pd.DataFrame(stock_data)

clients_df = st.session_state.clients_df
stock_df = st.session_state.stock_df

st.title("Gestion des Clients et du Stock")

# Display the clients table
st.header("Tableau des Clients")
st.dataframe(clients_df)

# Display the stock table
st.header("Tableau du Stock")
st.dataframe(stock_df)

# Form to add a client and check stock
st.header("Ajouter un Client et Vérifier le Stock")

with st.form(key='add_client'):
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    article = st.selectbox("Article", stock_df['Article'].tolist())
    pdf = st.file_uploader("Télécharger un fichier PDF", type=["pdf"])
    submit_button = st.form_submit_button(label='Ajouter et Vérifier le Stock')

    if submit_button:
        # Check stock
        stock_quantite = stock_df.loc[stock_df['Article'] == article, 'Quantité'].values[0]
        if stock_quantite > 0:
            # Process PDF file
            if pdf is not None:
                pdf_data = pdf.getvalue()
            else:
                pdf_data = None

            # Add the client
            new_client = pd.DataFrame({'Nom': [nom], 'Prénom': [prenom], 'Article': [article], 'PDF': [pdf_data]})
            st.session_state.clients_df = pd.concat([st.session_state.clients_df, new_client], ignore_index=True)
            st.success(f"Client ajouté avec succès ! Article {article} disponible en stock.")
            
            # Update stock
            st.session_state.stock_df.loc[stock_df['Article'] == article, 'Quantité'] -= 1
        else:
            st.error(f"Article {article} en rupture de stock !")

# Form to add or update stock
st.header("Ajouter ou Mettre à Jour le Stock")

with st.form(key='add_stock'):
    new_article = st.text_input("Nouvel Article")
    quantity = st.number_input("Quantité", min_value=1, step=1)
    submit_stock_button = st.form_submit_button(label='Ajouter/Mettre à Jour le Stock')

    if submit_stock_button:
        if new_article in stock_df['Article'].values:
            # Update existing stock
            st.session_state.stock_df.loc[stock_df['Article'] == new_article, 'Quantité'] += quantity
            st.success(f"Quantité de l'article {new_article} augmentée de {quantity}.")
        else:
            # Add new stock item
            new_stock_item = pd.DataFrame({'Article': [new_article], 'Quantité': [quantity]})
            st.session_state.stock_df = pd.concat([st.session_state.stock_df, new_stock_item], ignore_index=True)
            st.success(f"Nouvel article {new_article} ajouté avec une quantité de {quantity}.")

# Display the updated tables
st.header("Tableau des Clients mis à jour")
st.dataframe(st.session_state.clients_df)

st.header("Tableau du Stock mis à jour")
st.dataframe(st.session_state.stock_df)
