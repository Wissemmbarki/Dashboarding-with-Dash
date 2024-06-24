#########################################################################
###################### Bib ##############################################

import pandas as pd 
import numpy as np 
import plotly.express as px
import dash 
from dash import dcc
from dash import html
#import dash_core_components as dcc
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
#import dash_html_components as html
from dash.dependencies import Input, Output



dash.register_page(__name__, path='/distribution', name="Distribution 📊")

########################## Load Datast #######################
df = pd.read_csv('rapport_employe.csv')
df

############ Transposition du DataFrame #######################
rapport = df.transpose()
# Réinitialisation des index pour éviter la transposition de la colonne d'index
rapport.reset_index(inplace=True)
rapport.columns = rapport.iloc[0]  # Utilisation de la première ligne comme noms de colonnes
rapport = rapport[1:]  # Suppression de la première ligne qui contenait les noms de colonnes d'origine

######### Bar_fig ####################################################
bar_fig= px.bar(
  data_frame= rapport, x='Chiffre d\'affaires', y='Categories', color='Categories',
  orientation='h',title='Chiffre d\'affaires réalises par employe')
bar_fig.update_layout({'bargap':0.5})
bar_fig.show()

####################### clean up DataFrame #############################

# Créer un dictionnaire avec les types de données souhaités
types_dict = {'Trafic': int, 'Nb commande': int}
# Appliquer les types de données au DataFrame
rapport = rapport.astype(types_dict)

######################## Scatter_fig ###########################
scatter_fig = px.scatter(rapport, x = 'Nb commande', y = 'Trafic', color = 'Categories',
                          size ='Nb commande', title = 'Trafic Vs Nombre de commande  par employe')

scatter_fig

##### Chiffre d'affaire\\pourcentage colonnes Netoyage ################################
rapport['Chiffre d\'affaires'] = rapport['Chiffre d\'affaires'].str.replace(r'[\D]+', '', regex=True).astype(int)

percentage_columns = ['Taux engagement', 'Total réduction', 'Frais de livraison', 'Taux de transformation']
# Remove percentage symbols and convert to integers
rapport[percentage_columns] = rapport[percentage_columns].replace('%', '', regex=True).astype(float).astype(int)



################### TOP FLOP #####################################

rapport_sans_total = rapport.drop(rapport[rapport['Categories'] == 'Total'].index)
top_employe = rapport_sans_total.sort_values(by='Chiffre d\'affaires', ascending=False).iloc[0]['Categories']
flop_employe = rapport_sans_total.sort_values(by='Chiffre d\'affaires', ascending=True).iloc[0]['Categories']




######### APP #######################################################
#####################################################################

# Initialisation de l'application
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Fonction pour générer le graphique en secteurs (pie chart)
def generate_pie_chart(selected_percentage):
    fig = px.pie(rapport, names='Categories', values=selected_percentage, hole=0.3,
                 title=f'Répartition en pourcentage pour {selected_percentage}',
                 labels={'Categories': 'Catégorie', selected_percentage: 'Pourcentage'})
    return fig

# Mise en page du tableau de bord
layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col(html.Img(src='C:\\Users\\Kadhem\\Desktop\\baity\\baity_logo.jpg', style={'width': '80px', 'height': '80px', 'margin': 'auto'})),
        dbc.Col(html.H1('Graphiques de ventes', style={'text-align': 'center', 'font-family': 'Arial', 'margin-top': '20px', 'color': 'navy'})),
    ]),

    html.H4('Répartition en pourcentage par catégories', style={'font-family': 'Arial', 'margin-top': '20px'}),
    dcc.Graph(id="pie-chart"),
    html.P("Sélectionnez une variable de pourcentage :", style={'font-family': 'Arial'}),
    dcc.Dropdown(
        id='percentage-dropdown',
        options=[{'label': col, 'value': col} for col in percentage_columns],
        value=percentage_columns[0],
        multi=False,
        style={'width': '50%', 'font-family': 'Arial'}
    ),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=bar_fig)),
        ], style={'text-align': 'center', 'margin': 'auto', 'margin-top': '20px'}),

    html.Hr(),
    
    dbc.Row([
        dbc.Col(dcc.Graph(figure=scatter_fig)),
        ], style={'text-align': 'center', 'margin': 'auto', 'margin-top': '20px'}),

    html.Hr(),

    # Boîte noire pour afficher les résultats
    dbc.Row([
        dbc.Col(html.Span(children=[
            'Meilleur vendeur : ',
            html.P(top_employe, className="btn btn-dark m-2 fs-5"),
            
            html.Br(),
            html.Br(),
            
            'Vendeur le moins performant : ',
            html.P(flop_employe, className="btn btn-dark m-2 fs-5"),
            html.Br(),
        ]))
    ])
])

# Callback pour mettre à jour le graphique en secteurs en fonction de la sélection du menu déroulant
@callback(
    Output("pie-chart", "figure"),
    Input("percentage-dropdown", "value"))
def update_pie_chart(selected_percentage):
    return generate_pie_chart(selected_percentage)

#if __name__ == '__main__':
#    app.run_server(debug=True)
