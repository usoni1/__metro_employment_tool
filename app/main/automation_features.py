from flask import render_template
from . import main
from .. import db_connection
from pymongo import MongoClient
from bson import json_util
import json
from flask import request
import psycopg2
import pandas as pd
import csv
from sshtunnel import SSHTunnelForwarder

def get_conn():

    tunnel = SSHTunnelForwarder(
        ('104.196.253.120', 22),
        ssh_username='usoni1',
        ssh_private_key='/Users/utkarshsoni/ssh gcloud/gcloud_key',
        remote_bind_address=('localhost', 5432),
        local_bind_address=('localhost', 6543),  # could be any available port
    )

    tunnel.start()

    username = 'usoni1'
    password = 'password'
    database = '_metro_employment_tool_tables'
    conn = psycopg2.connect(host=tunnel.local_bind_host, user=username, password=password, dbname=database, port=tunnel.local_bind_port)
    return conn

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

    df = pd.read_csv('/PyCharm Projects/__metro_employment_tool/app/main/suit/ind_code.csv')
    ind_l = df['ind_code'].tolist()

    df = pd.read_csv('/PyCharm Projects/__metro_employment_tool/app/main/suit/msa_code.csv')
    msa_l = df['msa_code'].tolist()

    reader = csv.reader(open("/PyCharm Projects/__metro_employment_tool/app/main/suit/data.csv", "r"), delimiter=",")
    x = list(reader)

    all_lists.append(occ_list)
    all_lists.append(ind_list)
    all_lists.append(skill_list)
    all_lists.append(ind_l)
    all_lists.append(msa_l)
    all_lists.append(x)

    return json.dumps(all_lists, default=json_util.default)

@main.route('/get_all_msa_skill')
def get_all_msa_skill():
    conn = get_conn()
    skill_type = request.args.get('skill_type', False)
    skill_code = request.args.get('skill_code', False)

    cur = conn.cursor()
    cur.execute("SELECT "
                "msa, skill_info -> 'skill_data' ->> 'value' AS skill_value "
                "FROM _metro_employment_tool_tables.msa_skill_data "
                "WHERE skill_info ->> 'level' = '%s' AND skill_info -> 'skill_data' ->> 'skill' = '%s';" % (skill_type, skill_code))


    return json.dumps(list(cur.fetchall()), default=json_util.default)

@main.route('/get_all_zcta_skill')
def get_all_zcta_skill():
    conn = get_conn()
    skill_type = request.args.get('skill_type', False)
    skill_code = request.args.get('skill_code', False)

    cur = conn.cursor()
    cur.execute("SELECT "
                "zcta, skill_info -> 'skill_data' ->> 'value' AS skill_value "
                "FROM _metro_employment_tool_tables.zcta_skill_data "
                "WHERE skill_info ->> 'level' = '%s' AND skill_info -> 'skill_data' ->> 'skill' = '%s';" % (skill_type, skill_code))

    return json.dumps(list(cur.fetchall()), default=json_util.default)

@main.route('/get_zcta_loss_stats')
def get_zcta_loss_stats():

    MONGO_URL = 'mongodb://heroku_b1bgtk2f:7dqp31jt6it71sn00k93ku7v77@ds153494.mlab.com:53494/heroku_b1bgtk2f'
    client = MongoClient(MONGO_URL)
    db_mongo = client.get_database()

    loss_type = request.args.get('loss_type', False)
    if loss_type == "occupation_loss":
        occ_id = request.args.get('loss_holder', False)
        if occ_id != False:
            zcta_occ_loss_collection = db_mongo.zcta_occupation_loss
            zcta_occ_loss_complete = list(zcta_occ_loss_collection.aggregate
                ([
                {'$project': {
                    "_id": 0,
                    "zcta_id": 1,
                    "display": "$occ_loss_proportion." + occ_id
                }}
            ]
            ))
            return json.dumps(zcta_occ_loss_complete, default=json_util.default)
    elif loss_type == "industry_loss":
        ind_id = request.args.get('loss_holder', False)
        if ind_id != False:
            zcta_ind_loss_collection = db_mongo.zcta_industry_loss
            zcta_ind_loss_complete = list(zcta_ind_loss_collection.aggregate
                ([
                {'$project': {
                    "_id": 0,
                    "zcta_id": 1,
                    "display": "$ind_loss_proportion." + ind_id
                }}
            ]
            ))
            return json.dumps(zcta_ind_loss_complete, default=json_util.default)
    elif loss_type == "skill_loss":
        skill_id = request.args.get('loss_holder', False)
        if skill_id != False:
            zcta_skill_loss_collection = db_mongo.zcta_skill_loss
            zcta_ind_loss_complete = list(zcta_skill_loss_collection.aggregate
                ([
                {'$project': {
                    "_id": 0,
                    "zcta_id": 1,
                    "display": "$total_skill_loss.loss_skill_" + skill_id.replace('.', '_')
                }}
            ]
            ))
            return json.dumps(zcta_ind_loss_complete, default=json_util.default)
    else:
        return "Unknown loss_type"

    return "SERVER ERROR"

@main.route('/get_radar_chart')
def get_radar_chart():
    return render_template("radar.html")

@main.route('/get_two_zcta_skills')
def get_two_zcta_skills():
    conn = get_conn()
    zcta1 = request.args.get('zcta1', False)
    zcta2 = request.args.get('zcta2', False)
    zcta_list = []
    cur = conn.cursor()

    for t in [zcta1, zcta2]:
        cur.execute("SELECT "
                    "skill_info -> 'skill_data' ->> 'skill' as skill, skill_info -> 'skill_data' ->> 'value' AS skill_value "
                    "FROM _metro_employment_tool_tables.zcta_skill_data "
                    "WHERE skill_info ->> 'level' = 'LV' AND zcta = %d" % (
                    int(t)))
        t2 = []
        for z in list(cur.fetchall()):
            t1 = {
                "axis" : None,
                "value" : None
            }
            t1["axis"] = z[0]
            t1["value"] = float(z[1])
            t2.append(t1)
        zcta_list.append(t2)

    return json.dumps(zcta_list, default=json_util.default)

if __name__ == '__main__':
    pass