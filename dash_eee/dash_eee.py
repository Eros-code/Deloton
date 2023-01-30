from dash import Dash, html
from dash_bootstrap_templates import load_figure_template
import dash
import plotly.express as px
import dash_bootstrap_components as dbc

image_path='assets/deloton.png'

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

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


app.layout=html.Div(
    children=[
        html.Img(src=image_path, style={'width':'30%', 'height':'50%', "float":"right"}),
        html.H1("CURRENT RIDE", className="display-1, text-decoration-underline", style={'text-align':'center', 'font-family': "Helvetica", 'color':"#8cd98c"}),
        html.Div(className='container', style={'background-color':'#333333'}, children=[
            row]),
        html.Hr(style={"width": "100%", "height": "5px"}),
    html.Div(style={'background-color':'#333333'}, children=[
        row,
    ]),
    html.Div(
            children=[
                html.H3("RECENT RIDES", style={"text-align":"left", 'font-family': "Helvetica", 'color':"#8cd98c"}, className="display-1, text-decoration-underline"),
    ]),
    html.Div(row2)
])

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port=8080)

