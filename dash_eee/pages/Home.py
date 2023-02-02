from dash import Dash, html, Input, Output, dcc
from dash_bootstrap_templates import load_figure_template
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import json
import os

old_path = os.getcwd()
os.chdir("..")

new_path = os.getcwd() + '/app/Data/users_data.json'

with open(new_path, 'r') as f:
   data = json.load(f)

os.chdir(old_path)


user_list = []
for i in data:
    user = f'{i["first_name"]} {i["last_name"]}, user id: {i["user_id"]}'
    user_list.append(user)


image_path='assets/deloton.png'
dropdowns = html.Div(
    [
        dcc.Dropdown(
            options=user_list,
            id = 'first-dropdown'
        )],
)

card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Card title", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
            ]
        ),
    ],
    style={"width": "29rem"},
)

row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.H4("some text")),
                dbc.Col(html.H4("some text")),
                dbc.Col(html.H4("some text")),
            ]
        ),
    ]
)

row2 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(card)),
                dbc.Col(html.Div(card)),
                dbc.Col(html.Div(card)),
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
                dbc.Col(dropdowns)])], style={'background-color': '#303030'}),
                html.Hr(style={"width": "56%", "height": "10px"}),
        html.Br(),
    html.Div(children=[
        html.Hr(style={"width": "100%", "height": "5px"}),
        row,
        row,
        html.Hr(style={"width": "100%", "height": "5px"}),
    ]),

    html.Br(),
    html.Div(row2)
])