from flask import render_template
from . import main
from .. import db_connection
from pymongo import MongoClient
from bson import json_util
import json

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/get_all_lists')
def get_all_lists():
    MONGO_URL = 'mongodb://heroku_b1bgtk2f:7dqp31jt6it71sn00k93ku7v77@ds153494.mlab.com:53494/heroku_b1bgtk2f'
    client = MongoClient(MONGO_URL)
    db_mongo = client.get_database()
    all_lists = []

    occ_lists_collection = db_mongo.all_lists
    list_obj = occ_lists_collection.find_one({'list_id': 'occ_list_mag'})
    occ_list = list_obj['list_items']

    ind_lists_collection = db_mongo.all_lists
    list_obj = ind_lists_collection.find_one({'list_id': 'ind_list_mag'})
    ind_list = list_obj['list_items']

    ind_lists_collection = db_mongo.all_lists
    list_obj = ind_lists_collection.find_one({'list_id': 'skill_list_mag'})
    skill_list = list_obj['list_items']

    all_lists.append(occ_list)
    all_lists.append(ind_list)
    all_lists.append(skill_list)

    return json.dumps(all_lists, default=json_util.default)