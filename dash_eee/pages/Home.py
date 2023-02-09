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

# from main import k_stream




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
                dcc.Graph(id='example-graph')
            ]
        ),
    ],
    style={"width": "29rem"},
)


# k_log = k_stream()

user = {"user_id":3600,"name":"Molly Richards","gender":"female","address":"Flat 92y,Stokes cove,New Henry,HX6 8HS","date_of_birth":9849600000,"email_address":"molly_r4@gmail.com","height_cm":158,"weight_kg":49,"account_create_date":1638835200000,"bike_serial":"SN0000","original_source":"google ads"}
ride = ''
telemetry = ''

# if 'Data' in k_log:
#     user = k_log
# elif 'Telemetry' in k_log:
#     telemetry = k_log
# elif 'Ride' in k_log:
#     ride = k_log


row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.P(f'{user["user_id"]}')),
                dbc.Col(html.P(f'{telemetry}')),
                dbc.Col(html.P(f'{ride}')),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.P("some text")),
                dbc.Col(html.P("some text")),
                dbc.Col(html.P("some text")),
            ])
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
                dbc.Col(html.Div(children=[html.Br(), row]))])], style={'background-color': '#303030'}),
                html.Hr(style={"width": "56%", "height": "10px"}),
    html.Br(),
    html.Div(row2),
    # dcc.Interval(
    #         id='interval-component',
    #         interval=1*1000, # in milliseconds
    #         n_intervals=0
    #     )
])

# @app.callback(Output('live-update-text', 'children'),
#               Input('interval-component', 'n_intervals'))
# def update_metrics(n):
#     lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
#     style = {'padding': '5px', 'fontSize': '16px'}
#     return [
#         html.Span('Longitude: {0:.2f}'.format(lon), style=style),
#         html.Span('Latitude: {0:.2f}'.format(lat), style=style),
#         html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
#     ]