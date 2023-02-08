import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import datetime
from datetime import datetime, timedelta
from fpdf import FPDF
import imageio as iio
import kaleido
import numpy as np
import pgeocode
from PIL import Image, ImageOps
from assets.sql_wrapper import SQLConnection
import os
import dotenv

# Reading data. **Needs to be changed to read from RDS**
# user_df = pd.read_json('./Data/users_data.json')
# ride_df = pd.read_json('./Data/ride_data.json')
# recent_rides_df = ride_df[(ride_df['start_time'] > datetime.now() - timedelta(hours = 24)) & (ride_df['start_time'] < datetime.now())]

# Read data from RDS.

dotenv.load_dotenv(override=True)

dbname = os.environ["DBNAME"]
username = os.environ['SQL_USERNAME']
host = os.environ['SQL_HOST']
password = os.environ['SQL_PASSWORD']
sql = SQLConnection(dbname, username, password)

user_df = sql.q('SELECT * FROM users')
rides_df = sql.q('SELECT * FROM users')

# Processing
max_individual_recent_rides = recent_rides_df.groupby(['start_time']).max()
mean_individual_recent_rides = recent_rides_df.groupby(['start_time']).mean()
max_individual_rides_male = max_individual_recent_rides[max_individual_recent_rides['gender'] == 'male']
max_individual_rides_female = max_individual_recent_rides[max_individual_recent_rides['gender'] == 'female']
gender_counts = pd.DataFrame([['Male', len(max_individual_rides_male)], ['Female', len(max_individual_rides_female)]], columns = ['Gender', 'Count'])
total_riders = gender_counts['Count'].sum()
avg_power = round(recent_rides_df['power'].mean(), 2)
recent_rides_df[recent_rides_df['heart_rate'] == 0] = np.nan
avg_hrt = round(recent_rides_df['heart_rate'].mean())

# Figure creation

# Gender split pie chart
fig1 = px.pie(gender_counts, values='Count', names='Gender', title="Gender Split of Today's Rides")
fig1.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})
fig1.update_traces(marker_colors=['#7fc37f', '#333333'])
fig1.write_image("./daily_report/images/gender_counts.png")

# Age count histogram
fig2 = px.histogram(max_individual_recent_rides, x = 'age', nbins = 10, color= 'gender', title = "Age of Cyclists of Today's Rides", color_discrete_sequence=['#7fc37f', '#333333'])
fig2.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})
fig2.write_image("./daily_report/images/age.png")

# User locations
nomi = pgeocode.Nominatim('gb')
user_df["latitude"] = user_df["postcode"].apply(lambda x: nomi.query_postal_code(x[:-3])[9])
user_df["longitude"] = user_df["postcode"].apply(lambda x: nomi.query_postal_code(x[:-3])[10])
fig5 = px.scatter_mapbox(user_df, lat="latitude", lon="longitude", zoom=3.5, height=300, center=dict(lat=54, lon=0))
fig5.update_layout(mapbox_style="open-street-map")
fig5.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig5.write_image("./daily_report/images/map.png")
ImageOps.expand(Image.open('./daily_report/images/fig5.png'),border=2,fill='#7fc37f').save('./daily_report/images/map.png')

# PDF layout
# Margin
m = 10 
# Page width
pw = 210 - 2*m 

pdf = FPDF()

pdf.add_page()
pdf.set_font('Arial', 'B', 18)
pdf.cell(w=(pw/2), h=35, txt=f"Daily Report: {datetime.now().date().strftime('%d-%m-%Y')}", border=0, ln=0)
pdf.image('./daily_report/images/Deloton.png', 
          x = pw/2, y = None, w = 100, h = 0, type = 'PNG')
pdf.cell(w = pw, h = 10, txt='', border = 0, ln = 1)
pdf.set_font('Arial','',  11)
pdf.multi_cell(w=0, h=5, txt = f"Total number of riders: {total_riders}" + '\n' + f"Average power produced per rider: {avg_power} W" + '\n' + f"Average heart rate: {avg_hrt} BPM", border=0)
pdf.cell(w = pw, h = 90, txt='', border = 0, ln = 1)
pdf.cell(w = pw, h = 10, txt="Locations of today's rides:", border = 0, ln = 1)
pdf.cell(w = pw, h = 95, txt='', border = 0, ln = 1)
pdf.image('./daily_report/images/gender_counts.png', 
          x = m, y =80, w = pw/2 -0.5, h = 0, type = 'PNG')
pdf.image('./daily_report/images/age.png', 
          x = pw/2 + 0.5, y = 80, w = pw/2, h = 0, type = 'PNG')
pdf.image('./daily_report/images/map.png', 
          x = m, y = 175, w = pw, h = 0, type = 'PNG')
pdf.set_font('Arial','',  8)
pdf.cell(w = pw, h = 5, txt='Powered by Sigma Labs XYZ: Triple-E', border = 0, ln = 0, align='R')

pdf.output('./daily_report/daily_report.pdf', 'F')