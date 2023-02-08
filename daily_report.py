import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import datetime
from datetime import datetime, timedelta
from fpdf import FPDF


# Reading data. Needs to be changed to read from RDS
user_df = pd.read_json('./app/Data/users_data.json')
ride_df = pd.read_json('./app/Data/ride_data.json')
recent_rides_df = ride_df[(ride_df['start_time'] > datetime.now() - timedelta(hours = 24)) & (ride_df['start_time'] < datetime.now())]

max_individual_recent_rides = recent_rides_df.groupby(['start_time']).max()
mean_individual_recent_rides = recent_rides_df.groupby(['start_time']).mean()
max_individual_rides_male = max_individual_recent_rides[max_individual_recent_rides['gender'] == 'male']
max_individual_rides_female = max_individual_recent_rides[max_individual_recent_rides['gender'] == 'female']

gender_counts = pd.DataFrame([['Male', len(max_individual_rides_male)], ['Female', len(max_individual_rides_female)]], columns = ['Gender', 'Count'])
fig = px.pie(gender_counts, values='Count', names='Gender', title='Number of Recent Rides per Gender')
fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})
fig.update_layout(font_color = 'white')
fig.update_traces(marker_colors=['#7fc37f', '#fefee2'])

fig2 = px.histogram(max_individual_recent_rides, x = 'age', nbins = 10, color= 'gender', title = 'Age of Cyclists for Recent Rides', color_discrete_sequence=['#7fc37f', '#fefee2'])
fig2.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})
fig2.update_layout(font_color = 'white')

fig3 = px.histogram(mean_individual_recent_rides, x = 'power', nbins = 10, title = 'Test', color_discrete_sequence=['#7fc37f', '#fefee2'])
fig3.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})
fig3.update_layout(font_color = 'white')

fig4 = px.histogram(mean_individual_recent_rides, x = 'heart_rate', nbins = 10, title = 'Test', color_discrete_sequence=['#7fc37f', '#fefee2'])
fig4.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})
fig4.update_layout(font_color = 'white')

graphs = [fig, fig2, fig3, fig4]

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297
        
    def header(self):
        # Custom logo and positioning
        # Create an `assets` folder and put any wide and short image inside
        # Name the image `logo.png`
        self.image('Deloton.png', 10, 8, 33)
        self.set_font('Arial', 'B', 11)
        self.cell(self.WIDTH - 80)
        self.cell(60, 1, 'Sales report', 0, 0, 'R')
        self.ln(20)
        
    def footer(self):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def page_body(self, images):
        # Determine how many plots there are per page and set positions
        # and margins accordingly
        if len(images) == 3:
            self.image(images[0], 15, 25, self.WIDTH - 30)
            self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
            self.image(images[2], 15, self.WIDTH / 2 + 90, self.WIDTH - 30)
        elif len(images) == 2:
            self.image(images[0], 15, 25, self.WIDTH - 30)
            self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
        else:
            self.image(images[0], 15, 25, self.WIDTH - 30)
            
    def print_page(self, images):
        # Generates the report
        self.add_page()
        self.page_body(images)


pdf = PDF()

for elem in graphs:
    pdf.print_page(elem)
    
pdf.output('SalesRepot.pdf', 'F')