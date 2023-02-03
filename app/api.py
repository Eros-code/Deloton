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
@app.route("/ride/<int:user_id>", methods=["GET"])
def get_user_ride(user_id):
    df_filter = filter(lambda df_filter: df_filter["user_id"] == user_id, ride_data)
    return(dumps(list(df_filter)))

#Get rider information (e.g. name, gender, age, avg. heart rate, number of rides):
@app.route("/rider/<int:user_id>", methods=["GET"])
def get_user(user_id):
    df_filter = filter(lambda df_filter: df_filter["user_id"] == user_id, user_data)
    return(dumps(list(df_filter)))

# # Get all rides for a rider with a specific ID
@app.route("/rider/<int:user_id>/rides", methods=["GET"])
def get_user_rides(user_id):
    df_filter = filter(lambda df_filter: df_filter["user_id"] == user_id, ride_data)
    return(json.dumps(list(df_filter)))


# # Get all rides for a specific date
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



#     query = """SELECT * FROM title_url_des WHERE description = '%s';""" %(result)
#     tag_dict = {"story_by_tag" : db_select(query)}
#   else:
#     result_arr = result.split(",")
#     query = """SELECT * FROM title_url_des WHERE description = '%s' """ %(result_arr[0])
#     for i in range(1, len(result_arr)):
#       or_string = """OR description = '%s' """ %(result_arr[i])
#       query += or_string
#     query += ";"
#     tag_dict = {"story_by_tag" : db_select(query)}
  
#   return jsonify(tag_dict)


####################################################################################
###                                                                              ###
### DELETE /ride/:id                                                             ###
### Delete a with a specific ID ###                                              ###
###                                                                              ###
####################################################################################

#http://127.0.0.1:5000/search?tags=Europe
# GET /daily?date=01-01-2020 test

# @app.route("/stories", methods=["GET"])
# def stories():
#   query = """SELECT stories.*,
#   SUM(CASE direction WHEN 'up' THEN 1 WHEN 'down' THEN -1 ELSE 0 END) AS score
#   FROM stories
#   LEFT JOIN votes ON votes.story_id = stories.id
#   GROUP BY stories.id;"""
#   stories_dict = {"stories" : db_select(query)}
#   return jsonify(stories_dict)