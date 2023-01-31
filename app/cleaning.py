import json
import pandas as pd
import re 
import ast
import datetime
from datetime import date

data_json = json.load(open('data.json', 'r'))

user_df_columns=['user_id', 'first_name', 'last_name', 'gender', 'street', 'area', 'postcode', 'd_o_b', 'email', 'height', 'weight', 'account_creation_date']
user_df = pd.DataFrame(columns=user_df_columns)
ride_df = pd.DataFrame(columns=['user_id', 'start_time', 'serial_no', 'source', 'duration', 'resistance', 'heart_rate', 'rpm', 'power'])
data_regex = re.compile(r'{[\s\S]*}')
numbers_regex = re.compile(r'\d\.?\d*')

def df_creation():
    for log in data_json:
        if 'Getting user data from server' in log['log']:
            start_time = log['log'].split(' ')[1]
        if 'data = ' in log['log']:
            data = data_regex.findall(log['log'])
            user_dict = ast.literal_eval(data[0])
            if user_dict['user_id'] not in user_df['user_id'].unique():
                name = user_dict['name'].split(' ')
                address = user_dict['address'].split(',')
                user = [user_dict['user_id'], name[0], name[1], user_dict['gender'], address[0], address[1], address[2], user_dict['date_of_birth'], user_dict['email_address'], user_dict['height_cm'], user_dict['weight_kg'], user_dict['account_create_date']]
                user_df.loc[len(user_df)] = user
        elif 'Ride -' in log['log']:
            ride_data = numbers_regex.findall(log['log'])
        elif 'Telemetry -' in log['log']:
            telemetry_data = numbers_regex.findall(log['log'])
            ride = [user_dict['user_id'], start_time, user_dict['bike_serial'], user_dict['original_source'], ride_data[-2], ride_data[-1], telemetry_data[-3], telemetry_data[-2], telemetry_data[-1]]
            ride_df.loc[len(ride_df)] = ride

    return user_df, ride_df

user_df, ride_df = df_creation()

print(user_df)
print(ride_df)