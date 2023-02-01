import json
import pandas as pd
import re 
import ast
import datetime
from datetime import date

data_json = json.load(open('data.json', 'r'))

def df_creation():
    data_regex = re.compile(r'{[\s\S]*}')
    numbers_regex = re.compile(r'\d+\.?\d*')
    stop_words = ['Mr', 'Dr', 'Mrs', 'Miss']
    existing_user = set()
    user_rows = []
    ride_rows = []
    for log in data_json:
        if 'Getting user data from server' in log['log']:
            start_date = log['log'].split(' ')[0]
            start_year = start_date.split('-')[0]
            start_month = start_date.split('-')[1]
            start_day = start_date.split('-')[2]
            start_time = log['log'].split(' ')[1]
        if 'data = ' in log['log']:
            data = data_regex.findall(log['log'])
            user_dict = ast.literal_eval(data[0])
            if user_dict['user_id'] not in existing_user:
                existing_user.add(user_dict['user_id'])
                name = user_dict['name'].split(' ')
                if name[0] in stop_words:
                    name.pop(0)
                address = user_dict['address'].split(',')
                user_row = [user_dict['user_id'], name[0], name[1], user_dict['gender'], address[0], address[1], address[-1], datetime.datetime.fromtimestamp(user_dict['date_of_birth']/1000), user_dict['email_address'], user_dict['height_cm'], user_dict['weight_kg'], datetime.datetime.fromtimestamp(user_dict['account_create_date']/1000)]
                user_rows.append(user_row)
        elif 'Ride -' in log['log']:
            ride_data = numbers_regex.findall(log['log'])
        elif 'Telemetry -' in log['log']:
            telemetry_data = numbers_regex.findall(log['log'])
            ride_row = [user_dict['user_id'], start_year, start_month, start_day, start_time, user_dict['bike_serial'], user_dict['original_source'], ride_data[-2], ride_data[-1], telemetry_data[-3], telemetry_data[-2], telemetry_data[-1], user_dict['height_cm'], user_dict['weight_kg'], datetime.datetime.now().year - datetime.datetime.fromtimestamp(user_dict['date_of_birth']/1000).year]
            ride_rows.append(ride_row)

    user_df = pd.DataFrame(user_rows, columns=['user_id', 'first_name', 'last_name', 'gender', 'street', 'area', 'postcode', 'd_o_b', 'email', 'height', 'weight', 'account_creation_date'])
    ride_df = pd.DataFrame(ride_rows, columns=['user_id', 'start_year', 'start_month', 'start_day', 'start_time', 'serial_no', 'source', 'duration', 'resistance', 'heart_rate', 'rpm', 'power', 'height', 'weight', 'age'])
    return user_df, ride_df

user_df, ride_df = df_creation()

user_df.to_json('./Data/users_data.json')
ride_df.to_json('./Data/ride_data.json')