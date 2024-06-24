import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output

dash.register_page(__name__, path='/relationship', name="Relationship 📈")

####################### DATASET ################################
df = pd.read_csv("rapport_employe.csv")

#################################################################
######################## Clean Data##############################
# Transposition du DataFrame
rapport = df.transpose()
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

#################################################################
####################### SCATTER CHART #############################
def create_scatter_chart(x_axis="Categories", y_axis="Taux engagement (%)"):
    return px.scatter(data_frame=rapport, x=x_axis, y=y_axis, height=600)

####################### WIDGETS #############################
columns = ['Categories', 'Trafic', 'Taux engagement (%)', 'Nb devis', 'Nb commande',
       'Total réduction (%)', 'Frais de livraison (%)', 'Chiffre d\'affaires (TND)',
       'Taux de transformation (%)']

x_axis = dcc.Dropdown(id="x_axis", options=columns, value="Categories", clearable=False)
y_axis = dcc.Dropdown(id="y_axis", options=columns, value="Taux engagement (%)", clearable=False)
##################################################################################

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    "X-Axis", x_axis, 
    "Y-Axis", y_axis,
    dcc.Graph(id="scatter")
])

####################### CALLBACKS ###############################
@callback(Output("scatter", "figure"), [Input("x_axis", "value"),Input("y_axis", "value"), ])
def update_scatter_chart(x_axis, y_axis):
    return create_scatter_chart(x_axis, y_axis)

