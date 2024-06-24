
from dash import Dash, html, dcc
import dash
import plotly.express as px
from flask import Flask, jsonify
from app import app



# Créez une application Flask
server = Flask(__name__)

# Définissez une route API pour servir l'application Dash layout sous forme de données JSON via la méthode GET
@server.route('/api/dash', methods=['POST'])
def serve_dash_app():
    layout_json = app.layout.to_dict()  # Convertissez l'application Dash layout en dictionnaire JSON
    return jsonify(layout_json)  # Renvoyez le layout JSON

# Exécutez l'application Flask
if __name__ == '__main__':
    server.run(debug=True)