from dash import Dash, html, Input, Output
from dash_bootstrap_templates import load_figure_template
import dash
import plotly.express as px
import dash_bootstrap_components as dbc



image_path='https://user-images.githubusercontent.com/5181870/188019461-4a27a045-9301-4931-910c-b367f7b2709a.png'
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
    ], style = {'background-color': '#303030'}
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


layout2=html.Div(
    children=[
        html.Img(src=image_path, style={'width':'44%', 'height':'50%', "float":"right"}),
        html.Hr(style={"width": "56%", "height": "7px"}),
        html.Div(className='container', children=[
            html.Br(),
            dbc.Row( [
                dbc.Col(html.Div(html.H1("RECENT RIDES", className="display-1, text-decoration-underline", style={'text-align':'center','font-family': "Helvetica", 'color':"#8cd98c"}))),
                dbc.Col()])], style={'background-color': '#303030'}),
                html.Hr(style={"width": "56%", "height": "10px"}),
        html.Br(),
    html.Div(children=[

    html.Br()]),
    html.Div(row2)
])