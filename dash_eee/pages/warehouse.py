from dash import dcc, html, Output, Input, callback
import dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/warehouse')

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="This is a test",
                    className="header-title",
                    id='header_title',
                )])])
