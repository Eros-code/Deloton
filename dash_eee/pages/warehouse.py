from dash import dcc, html, Output, Input, callback
import dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/warehouse')

image_path='assets/deloton.png'
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


layout=html.Div(
    children=[
        html.Img(src=image_path, style={'width':'30%', 'height':'50%', "float":"right"}),
        html.H1("RECENT RIDES", className="display-1, text-decoration-underline", style={'text-align':'center', 'font-family': "Helvetica", 'color':"#8cd98c"}),
        html.Div(className='container', children=[
            row]),
        html.Hr(style={"width": "100%", "height": "5px"}),
    html.Div(children=[
        row,
        html.Hr(style={"width": "100%", "height": "5px"}),
    ]),
    html.Div(row2)
])