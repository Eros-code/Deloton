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

# Reading data. Needs to be changed to read from RDS
user_df = pd.read_json('./Data/users_data.json')
ride_df = pd.read_json('./Data/ride_data.json')
recent_rides_df = ride_df[(ride_df['start_time'] > datetime.now() - timedelta(hours = 24)) & (ride_df['start_time'] < datetime.now())]

max_individual_recent_rides = recent_rides_df.groupby(['start_time']).max()
mean_individual_recent_rides = recent_rides_df.groupby(['start_time']).mean()
max_individual_rides_male = max_individual_recent_rides[max_individual_recent_rides['gender'] == 'male']
max_individual_rides_female = max_individual_recent_rides[max_individual_recent_rides['gender'] == 'female']

gender_counts = pd.DataFrame([['Male', len(max_individual_rides_male)], ['Female', len(max_individual_rides_female)]], columns = ['Gender', 'Count'])
fig1 = px.pie(gender_counts, values='Count', names='Gender', title="Gender Split of Today's Rides")
fig1.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})
fig1.update_traces(marker_colors=['#7fc37f', '#333333'])
fig1.write_image("./daily_report/images/fig1.png")

fig2 = px.histogram(max_individual_recent_rides, x = 'age', nbins = 10, color= 'gender', title = 'Age of Cyclists for Recent Rides', color_discrete_sequence=['#7fc37f', '#333333'])
fig2.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})
fig2.write_image("./daily_report/images/fig2.png")

fig3 = px.histogram(mean_individual_recent_rides, x = 'power', nbins = 10 = 'Test', color_discrete_sequence=['#7fc37f', '#333333'])
fig3.update_layout({, title
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})
fig3.write_image("./daily_report/images/fig3.png")

fig4 = px.histogram(mean_individual_recent_rides, x = 'heart_rate', nbins = 10, title = 'Test', color_discrete_sequence=['#7fc37f', '#333333'])
fig4.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})
fig4.write_image("./daily_report/images/fig4.png")

total_riders = gender_counts['Count'].sum()
avg_power = round(recent_rides_df['power'].mean(), 2)
recent_rides_df[recent_rides_df['heart_rate'] == 0] = np.nan
avg_hrt = round(recent_rides_df['heart_rate'].mean())
# Margin
m = 10 
# Page width: Width of A4 is 210mm
pw = 210 - 2*m 

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 18)
# pdf.set_xy(x=10, y= 220) # or use pdf.ln(50)
pdf.cell(w=(pw/2), h=35, txt=f"Daily Report: {datetime.now().date().strftime('%d-%m-%Y')}", border=0, ln=0)
pdf.image('./daily_report/images/Deloton.png', 
          x = pw/2, y = None, w = 100, h = 0, type = 'PNG')
pdf.image('./daily_report/images/fig1.png', 
          x = pw/2, y = None, w = 100, h = 0, type = 'PNG')
pdf.set_font('Arial','',  11)
pdf.multi_cell(w=0, h=5, txt = f"Total number of riders: {total_riders}" + '\n' + f"Average power produced per rider: {avg_power} W" + '\n' + f"Average heart rate: {avg_hrt} BPM", border=0)
pdf.image('./daily_report/images/fig2.png', 
          x = m, y = None, w = 100, h = 0, type = 'PNG')
pdf.image('./daily_report/images/fig3.png', 
          x = m, y = None, w = 100, h = 0, type = 'PNG')
pdf.image('./daily_report/images/fig4.png', 
          x = m, y = None, w = 100, h = 0, type = 'PNG')
pdf.output('./daily_report/daily_report.pdf', 'F')