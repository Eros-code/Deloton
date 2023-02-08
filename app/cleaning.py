# Import libraries 
import json
import pandas as pd
import re 
import ast
import datetime

# Load data from Kafka. **NEEDS TO BE CHANGED TO READ FROM RDS**
data_json = data_json = json.load(open('Data/data.json', 'r'))

# Function creation for cleaning raw data and placing into  dataframe
def df_creation():
    # Text processing: regex search for data & stop word removal.
    data_regex = re.compile(r'{[\s\S]*}')
    numbers_regex = re.compile(r'\d+\.?\d*')
    stop_words = ['Mr', 'Dr', 'Mrs', 'Miss']

    # Loop to extract data from Kafka messages into lists.
    existing_user = set()
    user_rows = []
    ride_rows = []
    session_id = 0
    start_year = None
    start_month = None
    start_day = None 
    start_time = None
    age = None
    ride_data = [None, None, None, None]
    user_dict = {'user_id': None,
                'name': None,
                'gender': None,
                'date_of_birth': None,
                'bike_serial': None,
                'original_source': None,
                'height_cm': None,
                'weight_kg': None}

    for log in data_json:
        if 'Getting user data from server' in log['log']:
            start_date = log['log'].split(' ')[0]
            start_year = start_date.split('-')[0]
            start_month = start_date.split('-')[1]
            start_day = start_date.split('-')[2]
            start_time = log['log'].split(' ')[1]
            session_id += 1
        if 'data = ' in log['log']:
            data = data_regex.findall(log['log'])
            user_dict = ast.literal_eval(data[0])
            age = datetime.datetime.now().year - datetime.datetime.fromtimestamp(user_dict['date_of_birth']/1000).year
            if user_dict['user_id'] not in existing_user:
                existing_user.add(user_dict['user_id'])
                name = user_dict['name'].split(' ')
                if name[0] in stop_words:
                    name.pop(0)
                address = user_dict['address'].split(',')
                user_row = [user_dict['user_id'], name[0], name[1], user_dict['gender'], address[0], address[1], address[-1], str(datetime.datetime.fromtimestamp(user_dict['date_of_birth']/1000)), user_dict['email_address'], user_dict['height_cm'], user_dict['weight_kg'], str(datetime.datetime.fromtimestamp(user_dict['account_create_date']/1000))]
                user_rows.append(user_row)
        elif 'Ride -' in log['log']:
            ride_data = numbers_regex.findall(log['log'])
        elif 'Telemetry -' in log['log']:
            telemetry_data = numbers_regex.findall(log['log'])
            ride_row = [session_id, user_dict['user_id'], start_year, start_month, start_day, start_time, user_dict['bike_serial'], user_dict['original_source'], ride_data[-2], ride_data[-1], telemetry_data[-3], telemetry_data[-2], telemetry_data[-1], user_dict['height_cm'], user_dict['weight_kg'], age , user_dict['gender']]
            ride_rows.append(ride_row)

    # Dataframe creation from lists.
    user_df = pd.DataFrame(user_rows, columns=['user_id', 'first_name', 'last_name', 'gender', 'street', 'area', 'postcode', 'd_o_b', 'email', 'height', 'weight', 'account_creation_date'])
    ride_df = pd.DataFrame(ride_rows, columns=['session_id', 'user_id', 'start_year', 'start_month', 'start_day', 'start_time', 'serial_no', 'source', 'duration', 'resistance', 'heart_rate', 'rpm', 'power', 'height', 'weight', 'age', 'gender'])
    return user_df, ride_df

user_df, ride_df = df_creation()

# Write data to working directory. **NEEDS TO BE CHANGED TO WRITE TO RDS**
df1 = user_df.to_json(orient = 'records')
df2 = ride_df.to_json(orient = 'records')

parsed1 = json.loads(df1)
parsed2 = json.loads(df2)

user_json = json.dumps(parsed1, indent=4)

ride_json = json.dumps(parsed2, indent=4)

with open('Data/users_data.json', 'w') as f:
  f.write(user_json)

with open('Data/ride_data.json', 'w') as f:
  f.write(ride_json)