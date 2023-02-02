from dash import Dash, html, Input, Output, dcc
from dash_bootstrap_templates import load_figure_template
import dash
import plotly.express as px
import dash_bootstrap_components as dbc

image_path='assets/deloton.png'

dash_app = Dash(name=__name__, use_pages=True, routes_pathname_prefix="/dashapp/", external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Current-Ride", href="/dashapp/current-ride")),
        dbc.NavItem(dbc.NavLink("Recent-Rides", href="/dashapp/recent-rides")),
    ],
    brand="Navigation",
    color="#8cd98c",
    dark=True,
)

content = html.Div(id="page-content")

dash_app.layout=html.Div([dcc.Location(id="url"), navbar, content])

from pages.warehouse import layout2
from pages.Home import layout1
@dash_app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/dashapp/" or pathname == "/dashapp/current-ride":
        return layout1
    elif pathname == "/dashapp/recent-rides":
        return layout2
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

if __name__ == "__main__":
    dash_app.run_server(host="0.0.0.0", debug=True, port=8080)

