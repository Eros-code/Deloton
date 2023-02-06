from dash import Dash, html, Input, Output, dcc
from dash_bootstrap_templates import load_figure_template
import dash
import plotly.express as px
import dash_bootstrap_components as dbc

## import libraries needed to run dash app

image_path='assets/deloton.png'

## path to image

## setting pathname of dashapp to /dashapp/
dash_app = Dash(name=__name__, use_pages=True, routes_pathname_prefix="/dashapp/", external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)

## navigation bar added to the top with options current ride and recent ride
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Current-Ride", href="/dashapp/current-ride")),
        dbc.NavItem(dbc.NavLink("Recent-Rides", href="/dashapp/recent-rides")),
    ],
    brand="Navigation",
    color="#8cd98c",
    dark=True,
)

## create a container which holds the page content and load underneath navbar
content = html.Div(id="page-content")

dash_app.layout=html.Div([dcc.Location(id="url"), navbar, content])


## import the layout of each page and use callback to render the content
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

from pages import warehouse

## callbacks for dropdowns of each graph allowing change between both or male/female

## TODO: try and use one callback which can be accessed individually by each dropdown?

def dropdown_selector(figa, figb, figc, id):
    if id == "Both" :
        return figa
    elif id == "Male":
        return figb
    elif id == "Female":
        return figc

@dash_app.callback(
    Output("example-graph2", "figure"), 
    Input("genders1", "value"))

def update_graph1(genders1):
    return dropdown_selector(warehouse.fig2, warehouse.fig2b, warehouse.fig2c, genders1)

@dash_app.callback(
    Output("example-graph3", "figure"), 
    Input("genders2", "value"))

def update_graph2(genders2):
    return dropdown_selector(warehouse.fig3, warehouse.fig3b, warehouse.fig3c, genders2)

@dash_app.callback(
    Output("example-graph5", "figure"), 
    Input("genders3", "value"))

def update_graph3(genders3):
    return dropdown_selector(warehouse.fig5, warehouse.fig5b, warehouse.fig5c, genders3)

@dash_app.callback(
    Output("example-graph6", "figure"), 
    Input("genders4", "value"))

def update_graph4(genders4):
    return dropdown_selector(warehouse.fig6, warehouse.fig6b, warehouse.fig6c, genders4)


## running the dashapp on localhost as server

if __name__ == "__main__":
    dash_app.run_server(host="0.0.0.0", debug=True, port=8080)

