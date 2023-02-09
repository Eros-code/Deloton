from dash import Dash, html, Input, Output, dcc
from dash_bootstrap_templates import load_figure_template
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import json
import os

old_path = os.getcwd()
os.chdir("..")

new_path = os.getcwd() + '/app//Data/users_data.json'

with open(new_path, 'r') as f:
   data = json.load(f)

os.chdir(old_path)


image_path='assets/deloton.png'


card1 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Card title", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                dcc.Graph(id='live-update-graph', animate=True)
            ]
        ),
    ],
    style={"width": "29rem"},
)

card2 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Card title", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                dcc.Graph(id='live-update-graph2')
            ]
        ),
    ],
    style={"width": "29rem"},
)

card3 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Card title", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                dcc.Graph(id='live-update-graph3')
            ]
        ),
    ],
    style={"width": "29rem"},
)

row = html.Div(
    [
        dbc.Row(
            [   dbc.Col(html.P(id='live-update-text')),
                dbc.Col(html.P(id="live-update-text2")),
                dbc.Col(html.P(id="live-update-text3")),

            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.P(id='live-update-text4')),
                dbc.Col(html.P(id='live-update-text5')),
                dbc.Col(html.P(id='live-update-text6')),
            ])
    ]
)

row2 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(card1)),
                dbc.Col(html.Div(card2)),
                dbc.Col(html.Div(card3)),
            ]
        ),
    ]
)


layout1=html.Div(
    children=[
        html.Img(src=image_path, style={'width':'44%', 'height':'50%', "float":"right"}),
        html.Hr(style={"width": "56%", "height": "7px"}),
        html.Div(className='container', children=[
            html.Br(),
            dbc.Row( [
                dbc.Col(html.Div(html.H1("CURRENT RIDE", className="display-1, text-decoration-underline", style={'text-align':'center','font-family': "Helvetica", 'color':"#8cd98c"}))),
                dbc.Col(html.Div(children=[html.Br(), row]))])], style={'background-color': '#303030'}),
                html.Hr(style={"width": "56%", "height": "10px"}),
    html.Br(),
    dcc.Interval(
            id='interval-component',
            interval=2*1000, # in milliseconds
            n_intervals=0
        )
])
