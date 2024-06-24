import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output

dash.register_page(__name__, path='/survived', name="Survived Count 📊")

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

########################### DATE #####################################
rapport['Date'] = ['2023-10-01', '2023-11-01', '2023-12-01', '2024-01-01', '2024-02-01', '2024-03-01']
rapport['Date'] = pd.to_datetime(rapport['Date'])

########################################################################
########################################################################

# Définir les options de sélection de colonne pour le dropdown
dropdown_options = [{'label': col, 'value': col} for col in rapport.columns]


# Définir la disposition de l'application Dash
layout = html.Div([
    dcc.Dropdown(
        id='dropdown-column',
        options=dropdown_options,
        value="Trafic"  # Valeur initiale du dropdown
    ),
    dcc.Graph(id='line-plot')
])

# Définir la fonction de mise à jour du graphique en fonction de la sélection de colonne
@callback(
    Output('line-plot', 'figure'),
    [Input('dropdown-column', 'value')]
)
def update_graph(selected_column):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=rapport['Date'], y=rapport[selected_column], mode='lines', name=selected_column))
    fig.update_layout(title=f'{selected_column} en fonction du Date', xaxis_title='Date', yaxis_title=selected_column, template="plotly_dark")
    return fig