from dash import Dash, html, Input, Output, dcc
from dash_bootstrap_templates import load_figure_template
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
## libraries needed to run dash app

import os
import json
## os needed to obtain working directory

## libraries needed to process postcodes into locations for plotting on map
import pandas as pd
import pgeocode
from datetime import timedelta, datetime

## setting postcode processor to gb
nomi = pgeocode.Nominatim('gb')


## moving back from current directory to be able to access the Data folder
old_path = os.getcwd()
os.chdir("..")

print(os.getcwd())

## importing the data from local file 'data' needs to be accessed from rds or s3 bucket
## right now posing a security risk

new_path1 = os.getcwd() + '/app/Data/ride_data.json'
new_path2 = os.getcwd() + '/app/Data/users_data.json'

## set colours to black and green (same as company logo)
night_colors = ['#303030', '#8cd98c']

user_df = pd.read_json(new_path2)
ride_df = pd.read_json(new_path1)

## convert postcodes to latitude and longitude
user_df["latitude"] = user_df["postcode"].apply(lambda x: nomi.query_postal_code(x[:-3])[9])
user_df["longitude"] = user_df["postcode"].apply(lambda x: nomi.query_postal_code(x[:-3])[10])

os.chdir(old_path)


## get the past 12 hours of data
recent_rides_df = ride_df[(ride_df['start_time'] > datetime.now() - timedelta(hours = 12)) & (ride_df['start_time'] < datetime.now())]

## find max and mean counts for recent rides split into male and female

max_individual_recent_rides = recent_rides_df.groupby(['start_time']).max()
mean_individual_recent_rides = recent_rides_df.groupby(['start_time']).mean()
max_individual_rides_male = max_individual_recent_rides[max_individual_recent_rides['gender'] == 'male']
max_individual_rides_female = max_individual_recent_rides[max_individual_recent_rides['gender'] == 'female']

gender_counts = pd.DataFrame([['Male', len(max_individual_rides_male)], ['Female', len(max_individual_rides_female)]], columns = ['Gender', 'Count'])


## creating a list for the dropdown choice allowing for visualization 

choice_list_gender = ['Both', 'Male', 'Female']

##### creating graphs for now in this file but maybe look into moving to a different

fig1 = px.pie(gender_counts, values='Count', names='Gender', title='Number of Recent Rides per Gender')
fig1.update_traces(marker_colors=night_colors)


fig2 = px.histogram(max_individual_recent_rides, x = 'duration', nbins=10, color='gender', title = 'Duration of Recent Rides by Gender')
fig2b = px.histogram(max_individual_recent_rides[max_individual_recent_rides['gender'] == 'male'], x = 'duration', nbins=10, title = 'Duration of Recent Rides by male riders')
fig2c = px.histogram(max_individual_recent_rides[max_individual_recent_rides['gender'] == 'female'], x = 'duration', nbins=10, title = 'Duration of Recent Rides by female riders')

fig3 = px.histogram(max_individual_recent_rides, x = 'age', nbins = 10, color= 'gender', title = 'Age of Cyclists for Recent Rides')
fig3b = px.histogram(max_individual_recent_rides[max_individual_recent_rides['gender'] == 'male'], x = 'age', nbins = 10, title = 'Age of Cyclists for Recent Rides')
fig3c = px.histogram(max_individual_recent_rides[max_individual_recent_rides['gender'] == 'female'], x = 'age', nbins = 10, title = 'Age of Cyclists for Recent Rides')

fig4 = px.pie(recent_rides_df, values ='power', names='gender', title='Total Power Generated Recently per Gender')

fig5 = px.histogram(max_individual_recent_rides, x = 'power', nbins=10, color='gender', title = 'Power Generated in Recent Rides by Gender')
fig5b = px.histogram(max_individual_recent_rides[max_individual_recent_rides['gender'] == 'male'], x = 'power', nbins=10, color='gender', title = 'Power Generated in Recent Rides by Gender')
fig5c = px.histogram(max_individual_recent_rides[max_individual_recent_rides['gender'] == 'female'], x = 'power', nbins=10, color='gender', title = 'Power Generated in Recent Rides by Gender')

fig6 = px.histogram(max_individual_recent_rides, x = 'rpm', nbins=10, color='gender', title = 'RPM of Recent Rides by Gender')
fig6b = px.histogram(max_individual_recent_rides[max_individual_recent_rides['gender'] == 'male'], x = 'rpm', nbins=10, color='gender', title = 'RPM of Recent Rides by Gender')
fig6c = px.histogram(max_individual_recent_rides[max_individual_recent_rides['gender'] == 'female'], x = 'rpm', nbins=10, color='gender', title = 'RPM of Recent Rides by Gender')

fig7 = px.scatter_mapbox(user_df, lat="latitude", lon="longitude", zoom=3, height=300)
fig7.update_layout(mapbox_style="open-street-map")
fig7.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

image_path='https://user-images.githubusercontent.com/5181870/188019461-4a27a045-9301-4931-910c-b367f7b2709a.png'


## creating a function which initializes a card allowing for a graph to displayed

def card_creator(card_title:str, card_text:str, graph_id:str, figure:str, dropdown:bool, dropdown_options=None, dropdown_id=None):
    """
    This function allows you to initialise a card that displays a graph
    
    """

    ## if dropdown graph is initialized without a dropdown else initialize with dropdown
    if dropdown == False:
        card = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(card_title, className="card-title"),
                        html.P(
                            card_text,
                            className="card-text",
                        ),
                    dcc.Graph(id=graph_id, figure=figure)
                    ]
                ),
            ],
            style={"width": '29rem', "height":'40rem'},
        )
    elif dropdown == True:
        card = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(card_title, className="card-title"),
                        html.P(
                            card_text,
                            className="card-text",
                        ),
                    dcc.Dropdown(
                    id=dropdown_id,
                    options=dropdown_options,
                    style={
                    "background": "#8cd98c",
                    },
                    value="Both",
                    clearable=False
                    ),
                    dcc.Graph(id=graph_id, figure=figure)
                    ]
                ),
            ],
            style={"width": '29rem', "height":'40rem'},
        )
    return card


## {} means it is an empty figure - this is handled in the main script which updates the figure
card1 = card_creator(card_title='title', card_text='placeholder text', graph_id='example-graph1', figure=fig1, dropdown=False)
card2 = card_creator(card_title='title', card_text='placeholder text', graph_id='example-graph2', figure={}, dropdown=True, dropdown_options=choice_list_gender, dropdown_id='genders1')
card3 = card_creator(card_title='title', card_text='placeholder text', graph_id='example-graph3', figure={}, dropdown=True, dropdown_options=choice_list_gender, dropdown_id='genders2')
card4 = card_creator(card_title='title', card_text='placeholder text', graph_id='example-graph4', figure=fig4, dropdown=False)
card5 = card_creator(card_title='title', card_text='placeholder text', graph_id='example-graph5', figure={}, dropdown=True, dropdown_options=choice_list_gender, dropdown_id='genders3')
card6 = card_creator(card_title='title', card_text='placeholder text', graph_id='example-graph6', figure={}, dropdown=True, dropdown_options=choice_list_gender, dropdown_id='genders4')
card7 = card_creator(card_title='title', card_text='placeholder text', graph_id='delivery-map', figure=fig7,  dropdown=False)
card8 = card_creator(card_title='title', card_text='placeholder text', graph_id='example-graph7', figure={}, dropdown=False)
card9 = card_creator(card_title='title', card_text='placeholder text', graph_id='example-graph8', figure={}, dropdown=False)


## arranging the cards into 3 rows and 3 columns

row2 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(card1)),
                dbc.Col(html.Div(card2)),
                dbc.Col(html.Div(card3)),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(html.Div(card4)),
                dbc.Col(html.Div(card5)),
                dbc.Col(html.Div(card6)),
            ]),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(html.Div(card7)),
                dbc.Col(html.Div(card8)),
                dbc.Col(html.Div(card9)),
            ])
    ]
)

## bringing all the components above together to build the content of the page

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

    ]),
    html.Div(row2),
])
