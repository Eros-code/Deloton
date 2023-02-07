from flask import Flask, current_app, jsonify, request
import json
from json import load, dumps
from datetime import datetime
 
# Returns the current local date
current_time = datetime.now()

app = Flask(__name__)

# Load the user_df.json data into a dict
user_df = open("Data/users_data.json")
user_data = load(user_df) # pf

ride_df = open("Data/ride_data.json")
ride_data = load(ride_df)

@app.route("/", methods=["GET"])
def test():
    return "this is a test!"

# Get a ride with a specific ID:
@app.route("/ride/<int:session_id>", methods=["GET"])
def get_user_ride(session_id):
    df_filter = filter(lambda df_filter: df_filter["session_id"] == session_id, ride_data)
    return(dumps(list(df_filter)))

#Get rider information (e.g. name, gender, age, avg. heart rate, number of rides):
@app.route("/rider/<int:user_id>", methods=["GET"])
def get_user(user_id):
    df_filter = filter(lambda df_filter: df_filter["user_id"] == user_id, user_data)
    return(dumps(list(df_filter)))

#Get rider information by gender (e.g. name, gender, age, avg. heart rate, number of rides):
@app.route("/rider/<gender>", methods=["GET"])
def get_user_gender(gender):
    df_filter = filter(lambda df_filter: df_filter["gender"] == gender, user_data)
    return(dumps(list(df_filter)))

  
#Get rides by gender:
@app.route("/rides/<gender>", methods=["GET"])
def get_ride_gender(gender):
    df_filter = filter(lambda df_filter: df_filter["gender"] == gender, ride_data)
    return(dumps(list(df_filter)))

#Get rides by age or by an age range:
@app.route("/rides", methods=["GET"])
def get_ride_age():
    args = request.args
    result = args.get('age', type=str)
    if '-' not in result:
      df_filter = filter(lambda df_filter: df_filter["age"] == int(result), ride_data)
      return(dumps(list(df_filter)))
    else:
      result_arr = result.split("-")
      df_filter = filter(lambda df_filter: df_filter["age"] >= int(result_arr[0]) and df_filter["age"] <= int(result_arr[1]) , ride_data)
      return(dumps(list(df_filter)))

#Get all riders from specific location(s):
@app.route("/rider", methods=["GET"])
def locate_users():
    args = request.args
    result = args.get('location', type=str)

    if ',' not in result:
      df_filter = filter(lambda df_filter: df_filter["area"] == str(result), user_data)
      return(dumps(list(df_filter)))
    else:
      result_arr = result.split(",")
      location_list = []
      for i in range(0, len(result_arr)):
        df_filter = filter(lambda df_filter: df_filter["area"] == str(result_arr[i]), user_data)
        location_list.append({str(result_arr[i]):list(df_filter)})
    return(dumps(list(location_list)))

## Get all rides for a rider with a specific ID
@app.route("/rider/<int:user_id>/rides", methods=["GET"])
def get_user_rides(user_id):
    df_filter = filter(lambda df_filter: df_filter["user_id"] == user_id, ride_data)
    return(json.dumps(list(df_filter)))


## Get all rides for a specific date
@app.route("/daily", methods=["GET"])
def date():
  args = request.args
  result = args.get('date', type=str)
  current_year = current_time.year
  current_month = current_time.month
  current_day = current_time.day

  if result == None:
    current_year = current_time.year
    current_month = current_time.month
    current_day = current_time.day
    df_filter = filter(lambda record: (record["start_year"], record['start_month'], record['start_day']) == (str(current_year), str(current_month), str(current_day)), ride_data)
    return(dumps(list(df_filter)))

  if '-' not in result:
    #### filter by year ####
    df_filter = filter(lambda year: year["start_year"] == str(result), ride_data)
    return(dumps(list(df_filter)))
  elif '-' in result:
    result_arr = result.split("-")

    ### filter by year and month ###
    if len(result_arr) == 2:
      print(result_arr)
      df_filter = filter(lambda record: (record["start_year"], record['start_month']) == (str(result_arr[0]), str(result_arr[1])), ride_data)
      return dumps(list(df_filter))
    
    ### filter by year, month and day
    elif len(result_arr) > 2:
      print(result_arr)
      df_filter = filter(lambda record: (record["start_year"], record['start_month'], record['start_day']) == (result_arr[0], result_arr[1], result_arr[2]), ride_data)
      return dumps(list(df_filter))

# # delete a ride with a specific ID:
# @app.route("/ride/del/<int:session_id>", methods=["DELETE"])
# def delete_ride(session_id):
#     df_filter = filter(lambda df_filter: df_filter["session_id"] == session_id, ride_data)
#     return("Ride was successfully deleted")
  


#http://127.0.0.1:5000/search?tags=Europe
# GET /daily?date=01-01-2020 test
