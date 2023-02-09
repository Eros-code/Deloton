import re
import os
import json
import ast
import datetime

def get_msg(cons):
    messages = []
    while True:
        msg = cons.poll(0.0)
        if msg is None:
            break
        messages.append(json.loads(msg.value().decode('utf-8')))
    cons.commit()
    user = {"log":'data = {"user_id":3599,\"name\":\"Leigh Bennett\",\"gender\":\"female\",\"address\":\"286 Abbott manor,Port Bethanyton,G4 0GY\",\"date_of_birth\":-667612800000,\"email_address\":\"leigh_bennett@yahoo.com\",\"height_cm\":175,\"weight_kg\":67,\"account_create_date\":1638576000000,\"bike_serial\":\"SN0000\",\"original_source\":\"google ads\"}'}
    ride = {"log": ''}
    telemetry = {"log": ''}

    if messages != []:
        for i in messages:
            if messages != [] and 'Data = ' in i['log']:
                user = i
            elif messages != [] and 'Ride - ' in i['log']:
                ride = i
            elif messages != [] and 'Telemetry - ' in i['log']:
                telemetry = i

    data_list = [user, ride, telemetry]
    return data_list


def format_data(cons):

    user_dict = {'user_id': None,
                'name': None,
                'gender': None,
                'date_of_birth': None,
                'bike_serial': None,
                'original_source': None,
                'height_cm': None,
                'weight_kg': None}

    new_msg = get_msg(cons)
    user = new_msg[0]
    ride = new_msg[1]
    telemetry = new_msg[2]
    data_regex = re.compile(r'{[\s\S]*}')
    numbers_regex = re.compile(r'\d+\.?\d*')

    if 'data = ' in user['log']:
            data = data_regex.findall(user['log'])
            user_dict = ast.literal_eval(data[0])
            age = datetime.datetime.now().year - datetime.datetime.fromtimestamp(user_dict['date_of_birth']/1000).year
            name = user_dict['name']

    ride_data = numbers_regex.findall(ride['log'])
    telemetry_data = numbers_regex.findall(telemetry['log'])
    if len(ride_data) > 0:
        duration = ride_data[-2]
        resistance = ride_data[-1]
    else:
        duration = ''
        resistance = ''

    if len(telemetry_data) > 0:
        hrt = telemetry_data[-3]
        rpm = telemetry_data[-2]
        power = telemetry_data[-1]
    else:
        hrt = ''
        rpm = ''
        power = ''

    return name, age, user_dict['gender'], duration, resistance, hrt, rpm, power