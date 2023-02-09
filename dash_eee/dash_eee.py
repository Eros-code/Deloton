from dash import Dash, html, Input, Output, dcc
from dash_bootstrap_templates import load_figure_template
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
from main import kafka_consumer, format_data
from consumer import get_msg, format_data
import time
import plotly


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

from pages import warehouse

@dash_app.callback(
    Output("example-graph2", "figure"), 
    Input("genders1", "value"))

def update_graph1(genders1):
    if genders1 == "Both" :
        return warehouse.fig2
    elif genders1 == "Male":
        return warehouse.fig2b
    elif genders1 == "Female":
        return warehouse.fig2c

@dash_app.callback(
    Output("example-graph3", "figure"), 
    Input("genders2", "value"))

def update_graph2(genders2):
    if genders2 == "Both" :
        return warehouse.fig3
    elif genders2 == "Male":
        return warehouse.fig3b
    elif genders2 == "Female":
        return warehouse.fig3c

@dash_app.callback(
    Output("example-graph5", "figure"), 
    Input("genders3", "value"))

def update_graph3(genders3):
    if genders3 == "Both" :
        return warehouse.fig5
    elif genders3 == "Male":
        return warehouse.fig5b
    elif genders3 == "Female":
        return warehouse.fig5c

@dash_app.callback(
    Output("example-graph6", "figure"), 
    Input("genders4", "value"))

def update_graph4(genders4):
    if genders4 == "Both" :
        return warehouse.fig6
    elif genders4 == "Male":
        return warehouse.fig6b
    elif genders4 == "Female":
        return warehouse.fig6c

consumer = kafka_consumer()

@dash_app.callback(Output('live-update-text', 'children'),
                  Output('live-update-text2', 'children'),
                  Output('live-update-text3', 'children'),
                  Output('live-update-text4', 'children'),
                  Output('live-update-text5', 'children'),
                  Output('live-update-text6', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):

    name, age, gender,duration,resistance,hrt,rpm,power = format_data(consumer)

    return [
        html.Span(f'{name}'),
        html.Span(f'{age} years old'),
        html.Span(f'{gender}'),
        html.Span(f'{duration} SECS'),
        html.Span(f'{hrt} BPM'),
        html.Span(f'{round(float(power),2)}')
    ]

data = {
        'duration': [],
        'hrt': [],
        'rpm': [],
        'power': [],
    }

# @dash_app.callback(Output('live-update-graph', 'extendData'),
# Input('interval-component', 'n_intervals'))
# def update_graph_live(n):

#     name, age, gender,duration,resistance,hrt,rpm,power = format_data(consumer)

#     if duration != '' and hrt != '':
#         data['duration'].append(float(duration))
#         data['hrt'].append(int(hrt))
#     elif duration != '' or hrt != '':
#         data['duration'].append(0)
#         data['hrt'].append(0)

#     # data['rpm'].append(float(rpm))
#     # data['power'].append(float(power))

#     # hrt_fig = px.line(x = [0], y = [0], title = 'Heart Rate',
#     #                 labels = {'duration': 'Time (s)',
#     #                             'heart_rate': 'Heart Rate (BPM)'})

#     hrt_fig = px.line(x = data['duration'], y = data['hrt'], title = 'Heart Rate',
#                     labels = {'duration': 'Time (s)',
#                                 'heart_rate': 'Heart Rate (BPM)'})


#     hrt_fig.append_trace({
#         'x': data['duration'],
#         'y': data['hrt'],
#         'name': 'hrt',
#         'mode': 'lines+markers',
#         'type': 'scatter'
#     },1,1)


#     return hrt_fig

if __name__ == "__main__":
    dash_app.run_server(host="0.0.0.0", debug=True, port=8080)

