# This file read and push a json file in a list
# and insert it in a collection in a db.

import json
from pymongo import MongoClient

# connect to the MongoDB
connection = MongoClient("mongodb://localhost:27017/")

# connect to the UnilPlan database and the Classes collection
db = connection.db_unilplan.classes

# open .json, and make a list with them
with open('crawler/crawler/JSON_output_files/Courses.json', encoding='utf-8') as json_data:
    classes = {}
    classes = json.load(json_data)
    json_data.close()
    print(".json = ok")

# insert the data in the db
db.insert(classes)
print("correctly added")

# close the connection to MongoDB
connection.close()