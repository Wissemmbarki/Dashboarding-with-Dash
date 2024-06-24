import pandas as pd
import dash
from dash import html, dash_table, dcc
import plotly.graph_objects as go

dash.register_page(__name__, path='/dataset', name="Dataset 📋")

####################### LOAD DATASET #############################
rapport = pd.read_csv("rapport_employe.csv")
##################################################################
######################## Clean Data###############################
# Transposition du DataFrame
rapport = rapport.transpose()
# Réinitialisation des index pour éviter la transposition de la colonne d'index
rapport.reset_index(inplace=True)
rapport.columns = rapport.iloc[0]  # Utilisation de la première ligne comme noms de colonnes
rapport = rapport[1:]  # Suppression de la première ligne qui contenait les noms de colonnes d'origine


types_dict = {'Trafic': int, 'Nb commande': int}
rapport = rapport.astype(types_dict)

rapport['Chiffre d\'affaires'] = rapport['Chiffre d\'affaires'].str.replace(r'[\D]+', '', regex=True).astype(int)

percentage_columns = ['Taux engagement', 'Total réduction', 'Frais de livraison', 'Taux de transformation']

# Remove percentage symbols and convert to integers
rapport[percentage_columns] = rapport[percentage_columns].replace('%', '', regex=True).astype(float).astype(int)

new_columns = ['Categories', 'Trafic', 'Taux engagement (%)', 'Nb devis', 'Nb commande',
       'Total réduction (%)', 'Frais de livraison (%)', 'Chiffre d\'affaires (TND)',
       'Taux de transformation (%)']
rapport.columns = new_columns





####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    dash_table.DataTable(data=rapport.to_dict('records'),
                         page_size=20,
                         style_cell={"background-color": "lightgrey", "border": "solid 1px white", "color": "black", "font-size": "11px", "text-align": "left"},
                         style_header={"background-color": "dodgerblue", "font-weight": "bold", "color": "white", "padding": "10px", "font-size": "18px"},
                        ),
])