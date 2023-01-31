from dash import Dash, html, Input, Output, dcc
from dash_bootstrap_templates import load_figure_template
import dash
import plotly.express as px
import dash_bootstrap_components as dbc

image_path='assets/deloton.png'

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)
pages = list(dash.page_registry.values())

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Current-Ride", href="/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem(f"{pages[0]['name']}", href=pages[0]['relative_path'], active="exact"),
            ],
            nav=True,
            label="More",
        ),
    ],
    brand="Navigation",
    color="#8cd98c",
    dark=True,
)

content = html.Div(id="page-content")

app.layout= html.Div([dcc.Location(id="url"), navbar, content])

from pages import warehouse, Home
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return Home.layout
    elif pathname == "/warehouse":
        return warehouse.layout
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
    app.run_server(host="0.0.0.0", debug=True, port=8080)

