from flask import render_template
from . import main
from .. import db_connection
from pymongo import MongoClient
from bson import json_util
import json
from flask import request, jsonify
import psycopg2
import pandas as pd
import csv
from sshtunnel import SSHTunnelForwarder
import operator

def get_conn():

    # tunnel = SSHTunnelForwarder(
    #     ('104.196.253.120', 22),
    #     ssh_username='usoni1',
    #     ssh_private_key='/Users/utkarshsoni/ssh gcloud/gcloud_key',
    #     remote_bind_address=('localhost', 5432),
    #     local_bind_address=('localhost', 6543),  # could be any available port
    # )
    #
    # tunnel.start()
    #
    # username = 'usoni1'
    # password = 'password'
    # database = '_metro_employment_tool_tables'
    # conn = psycopg2.connect(host=tunnel.local_bind_host, user=username, password=password, dbname=database, port=tunnel.local_bind_port)

    hostname = 'localhost'
    username = 'usoni1'
    password = 'password'
    database = '_metro_employment_tool'
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=5432)
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

    df = pd.read_csv('C:\\Users\\usoni1\\PycharmProjects\\__metro_employment_tool\\app\\main\\suit\\ind_code.csv')
    ind_l = df['ind_code'].tolist()

    df = pd.read_csv('C:\\Users\\usoni1\\PycharmProjects\\__metro_employment_tool\\app\\main\\suit\\msa_code.csv')
    msa_l = df['msa_code'].tolist()

    reader = csv.reader(open("C:\\Users\\usoni1\\PycharmProjects\\__metro_employment_tool\\app\\main\\suit\\data.csv", "r"), delimiter=",")
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

@main.route('/get_zcta_loss_rank_stats')
def get_zcta_loss_rank_stats():
    MONGO_URL = 'mongodb://heroku_b1bgtk2f:7dqp31jt6it71sn00k93ku7v77@ds153494.mlab.com:53494/heroku_b1bgtk2f'
    client = MongoClient(MONGO_URL)
    db_mongo = client.get_database()

    zcta_id = request.args.get('zcta_id', False)
    loss_type = request.args.get('loss_type', False)
    if zcta_id != False:
        if loss_type == 'occ_loss':
            zcta_occ_loss_collection = db_mongo.zcta_occupation_loss
            zcta_occ_loss_complete = zcta_occ_loss_collection.find_one({"zcta_id": zcta_id})
            t1 = zcta_occ_loss_complete["occ_loss_proportion"]
            sorted_t1 = sorted(t1.items(), key=operator.itemgetter(1), reverse=True)
            return json.dumps(sorted_t1, default=json_util.default)
        elif loss_type == 'ind_loss':
            zcta_ind_loss_collection = db_mongo.zcta_industry_loss
            zcta_ind_loss_complete = zcta_ind_loss_collection.find_one({"zcta_id": zcta_id})
            t1 = zcta_ind_loss_complete["ind_loss_proportion"]
            sorted_t1 = sorted(t1.items(), key=operator.itemgetter(1), reverse=True)
            return json.dumps(sorted_t1, default=json_util.default)
        elif loss_type == 'skill_loss':
            zcta_skill_loss_collection = db_mongo.zcta_skill_loss
            zcta_skill_loss_complete = zcta_skill_loss_collection.find_one({"zcta_id": zcta_id})
            t1 = zcta_skill_loss_complete["total_skill_loss"]
            sorted_t1 = sorted(t1.items(), key=operator.itemgetter(1), reverse=True)
            return json.dumps(sorted_t1, default=json_util.default)
        else:
            return "invalid loss type"

@main.route('/get_msa_loss_rank_stats')
def get_msa_loss_rank_stats():
    t = {
        "43620": "0485086",
        "12260": "0485382",
        "20500": "0485027",
        "17460": "0485048",
        "33740": "0485335",
        "22900": "0485210",
        "12060": "0485051",
        "40060": "0485013",
        "45500": "0485205",
        "32420": "0485351",
        "11700": "0485309",
        "23540": "0485118",
        "19740": "0485143",
        "41900": "0485122",
        "18700": "0485326",
        "49340": "0485283",
        "14500": "0485257",
        "35980": "0485301",
        "18580": "0485268",
        "34900": "0485023",
        "46540": "0485306",
        "36140": "0485209",
        "27180": "0485338",
        "27740": "0485388",
        "25500": "0485006",
        "35100": "0485017",
        "20700": "0485044",
        "21340": "0485045",
        "25020": "0485354",
        "21500": "0485248",
        "41060": "0485298",
        "23420": "0485040",
        "20260": "0485377",
        "17420": "0485087",
        "19460": "0485310",
        "47300": "0485043",
        "33780": "0485395",
        "33700": "0485202",
        "16540": "0485303",
        "46340": "0485053",
        "20100": "0485008",
        "14740": "0485037",
        "24300": "0485213",
        "29700": "0485054",
        "43340": "0485249",
        "39660": "0485307",
        "15380": "0485324",
        "31540": "0485266",
        "10900": "0485085",
        "37460": "0485224",
        "13740": "0485201",
        "15680": "0485029",
        "13460": "0485340",
        "47220": "0485206",
        "39140": "0485345",
        "37340": "0485255",
        "31860": "0485392",
        "33540": "0485050",
        "34580": "0485028",
        "23460": "0485262",
        "42020": "0485361",
        "45940": "0485234",
        "41980": "0485323",
        "38300": "0485286",
        "40220": "0485019",
        "47900": "0485297",
        "49180": "0485140",
        "13900": "0485308",
        "29100": "0485031",
        "17780": "0485203",
        "41700": "0485032",
        "34980": "0485033",
        "40900": "0485251",
        "25980": "0485015",
        "10780": "0485012",
        "38220": "0485374",
        "11260": "0485373",
        "41420": "0485305",
        "28700": "0485363",
        "25220": "0485021",
        "13140": "0485339",
        "26820": "0485375",
        "45220": "0485004",
        "18880": "0485139",
        "11640": "0485083",
        "15540": "0485331",
        "25420": "0485281",
        "38900": "0485009",
        "41540": "0485016",
        "30460": "0485204",
        "30860": "0485381",
        "41180": "0485014",
        "39580": "0485020",
        "14260": "0485260",
        "45060": "0485035",
        "46220": "0485215",
        "19100": "0485007",
        "19820": "0485003",
        "17900": "0485120",
        "42200": "0485264",
        "19340": "0485295",
        "24220": "0485024",
        "17980": "0485284",
        "31080": "0485018",
        "38060": "0485353",
        "46140": "0485302",
        "31420": "0485254",
        "34100": "0485253",
        "34060": "0485034",
        "33340": "0485041",
        "18140": "0485226",
        "29180": "0485390",
        "30300": "0485296",
        "35380": "0485233",
        "41500": "0485259",
        "26620": "0485225",
        "44100": "0485282",
        "10540": "0485128",
        "38660": "0485138",
        "24580": "0485383",
        "46700": "0485379",
        "49020": "0485250",
        "27140": "0485258",
        "35300": "0485304",
        "21660": "0485022",
        "24500": "0485208",
        "42660": "0485207",
        "49420": "0485212",
        "11100": "0485355",
        "29340": "0485042",
        "14460": "0485387",
        "45300": "0485396",
        "40660": "0485142",
        "10420": "0485119",
        "27620": "0485132",
        "24020": "0485086",
        "24860": "0485382",
        "12020": "0485027",
        "25940": "0485048",
        "19300": "0485335",
        "13220": "0485210",
        "40380": "0485051",
        "44060": "0485013",
        "41940": "0485205",
        "22660": "0485351",
        "48900": "0485309",
        "13780": "0485118",
        "27980": "0485143",
        "29420": "0485122",
        "34820": "0485326",
        "31020": "0485283",
        "42100": "0485257",
        "29540": "0485301",
        "15180": "0485268",
        "13980": "0485023",
        "17140": "0485306",
        "16740": "0485209",
        "31340": "0485338",
        "30980": "0485388",
        "48060": "0485006",
        "12420": "0485017",
        "41620": "0485044",
        "44300": "0485045",
        "13380": "0485354",
        "26580": "0485248",
        "37980": "0485298",
        "49740": "0485040",
        "16700": "0485377",
        "13820": "0485087",
        "47460": "0485310",
        "30700": "0485043",
        "29620": "0485395",
        "18020": "0485202",
        "22020": "0485303",
        "12580": "0485053",
        "21780": "0485008",
        "16620": "0485037",
        "12700": "0485213",
        "28020": "0485054",
        "45780": "0485249",
        "26420": "0485307",
        "14100": "0485324",
        "46060": "0485266",
        "33260": "0485085",
        "19380": "0485224",
        "20220": "0485201",
        "14020": "0485029",
        "27500": "0485340",
        "29940": "0485206",
        "21140": "0485345",
        "38940": "0485255",
        "43100": "0485392",
        "22540": "0485050",
        "43780": "0485028",
        "12620": "0485262",
        "11540": "0485361",
        "16220": "0485234",
        "40980": "0485323",
        "13020": "0485286",
        "32900": "0485019",
        "39900": "0485297",
        "23900": "0485140",
        "21300": "0485308",
        "36780": "0485031",
        "41100": "0485203",
        "11180": "0485032",
        "12540": "0485033",
        "48140": "0485251",
        "26980": "0485015",
        "31700": "0485012",
        "22420": "0485374",
        "41660": "0485373",
        "12980": "0485305",
        "34620": "0485363",
        "19180": "0485021",
        "42140": "0485339",
        "48700": "0485375",
        "30140": "0485004",
        "34940": "0485139",
        "33220": "0485083",
        "11020": "0485331",
        "30620": "0485281",
        "36420": "0485009",
        "35620": "0485016",
        "14010": "0485204",
        "42680": "0485381",
        "34740": "0485014",
        "22520": "0485020",
        "39340": "0485260",
        "12220": "0485035",
        "19500": "0485215",
        "25260": "0485007",
        "49660": "0485003",
        "17660": "0485120",
        "30780": "0485264",
        "38860": "0485295",
        "16580": "0485024",
        "19780": "0485284",
        "33140": "0485018",
        "25620": "0485353",
        "29200": "0485302",
        "23060": "0485254",
        "30340": "0485253",
        "36740": "0485034",
        "43300": "0485041",
        "31180": "0485226",
        "27060": "0485390",
        "15260": "0485296",
        "15500": "0485233",
        "25540": "0485259",
        "33460": "0485225",
        "39380": "0485282",
        "26300": "0485128",
        "47940": "0485138",
        "32780": "0485383",
        "33100": "0485379",
        "47380": "0485250",
        "32820": "0485258",
        "24660": "0485304",
        "26900": "0485022",
        "42700": "0485208",
        "27900": "0485207",
        "11500": "0485212",
        "16860": "0485355",
        "28940": "0485042",
        "22220": "0485387",
        "22180": "0485396",
        "24340": "0485142",
        "39820": "0485119",
        "10740": "0485132",
        "49620": "0485086",
        "24420": "0485382",
        "46660": "0485027",
        "29460": "0485048",
        "40580": "0485335",
        "29020": "0485210",
        "14860": "0485051",
        "29740": "0485013",
        "19060": "0485205",
        "31140": "0485351",
        "36260": "0485309",
        "10500": "0485118",
        "29820": "0485143",
        "32580": "0485122",
        "41860": "0485326",
        "10380": "0485283",
        "48300": "0485257",
        "14540": "0485301",
        "26380": "0485268",
        "16020": "0485023",
        "48660": "0485306",
        "26140": "0485209",
        "27260": "0485338",
        "47580": "0485388",
        "42340": "0485006",
        "21060": "0485017",
        "12100": "0485044",
        "21820": "0485045",
        "20020": "0485354",
        "31460": "0485248",
        "44700": "0485298",
        "17020": "0485040",
        "41140": "0485377",
        "28740": "0485087",
        "28140": "0485310",
        "43580": "0485043",
        "10580": "0485395",
        "48620": "0485202",
        "39460": "0485303",
        "36540": "0485053",
        "46520": "0485008",
        "45820": "0485037",
        "22500": "0485213",
        "47020": "0485054",
        "36980": "0485249",
        "28420": "0485307",
        "36500": "0485324",
        "43900": "0485266",
        "17300": "0485085",
        "37860": "0485224",
        "16060": "0485201",
        "28660": "0485029",
        "44180": "0485340",
        "37900": "0485206",
        "16300": "0485345",
        "43420": "0485255",
        "10180": "0485392",
        "35840": "0485050",
        "27780": "0485028",
        "16940": "0485262",
        "24140": "0485361",
        "30020": "0485234",
        "15940": "0485323",
        "24260": "0485286",
        "48260": "0485019",
        "35660": "0485297",
        "40420": "0485140",
        "24540": "0485308",
        "19140": "0485031",
        "39740": "0485203",
        "39540": "0485032",
        "27340": "0485033",
        "17820": "0485251",
        "27860": "0485015",
        "38340": "0485012",
        "38540": "0485374",
        "42220": "0485373",
        "33860": "0485305",
        "25180": "0485363",
        "36100": "0485021",
        "49700": "0485339",
        "15980": "0485375",
        "20940": "0485004",
        "47260": "0485139",
        "25860": "0485083",
        "19660": "0485331",
        "40340": "0485281",
        "31740": "0485009",
        "16820": "0485016",
        "37100": "0485204",
        "41740": "0485381",
        "45460": "0485014",
        "45540": "0485020",
        "40140": "0485260",
        "42540": "0485035",
        "16980": "0485215",
        "37620": "0485007",
        "44940": "0485003",
        "22140": "0485120",
        "36220": "0485264",
        "44420": "0485295",
        "24780": "0485024",
        "25060": "0485284",
        "33660": "0485018",
        "22380": "0485353",
        "12940": "0485302",
        "17860": "0485254",
        "44140": "0485253",
        "48540": "0485034",
        "27100": "0485041",
        "31900": "0485226",
        "39300": "0485390",
        "16180": "0485296",
        "28100": "0485233",
        "20740": "0485259",
        "11460": "0485225",
        "23580": "0485282",
        "44220": "0485128"
    }

    MONGO_URL = 'mongodb://heroku_b1bgtk2f:7dqp31jt6it71sn00k93ku7v77@ds153494.mlab.com:53494/heroku_b1bgtk2f'
    client = MongoClient(MONGO_URL)
    db_mongo = client.get_database()

    zcta_id = t[request.args.get('msa_id', False)]
    loss_type = request.args.get('loss_type', False)
    if zcta_id != False:
        if loss_type == 'occ_loss':
            zcta_occ_loss_collection = db_mongo.zcta_occupation_loss
            zcta_occ_loss_complete = zcta_occ_loss_collection.find_one({"zcta_id": zcta_id})
            t1 = zcta_occ_loss_complete["occ_loss_proportion"]
            sorted_t1 = sorted(t1.items(), key=operator.itemgetter(1), reverse=True)
            return json.dumps(sorted_t1, default=json_util.default)
        elif loss_type == 'ind_loss':
            zcta_ind_loss_collection = db_mongo.zcta_industry_loss
            zcta_ind_loss_complete = zcta_ind_loss_collection.find_one({"zcta_id": zcta_id})
            t1 = zcta_ind_loss_complete["ind_loss_proportion"]
            sorted_t1 = sorted(t1.items(), key=operator.itemgetter(1), reverse=True)
            return json.dumps(sorted_t1, default=json_util.default)
        elif loss_type == 'skill_loss':
            zcta_skill_loss_collection = db_mongo.zcta_skill_loss
            zcta_skill_loss_complete = zcta_skill_loss_collection.find_one({"zcta_id": zcta_id})
            t1 = zcta_skill_loss_complete["total_skill_loss"]
            sorted_t1 = sorted(t1.items(), key=operator.itemgetter(1), reverse=True)
            return json.dumps(sorted_t1, default=json_util.default)
        else:
            return "invalid loss type"


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

@main.route('/get_msa_loss_stats')
def get_msa_loss_stats():

    MONGO_URL = 'mongodb://heroku_b1bgtk2f:7dqp31jt6it71sn00k93ku7v77@ds153494.mlab.com:53494/heroku_b1bgtk2f'
    client = MongoClient(MONGO_URL)
    db_mongo = client.get_database()

    t = {
    "43620":"0485086",
    "12260":"0485382",
    "20500":"0485027",
    "17460":"0485048",
    "33740":"0485335",
    "22900":"0485210",
    "12060":"0485051",
    "40060":"0485013",
    "45500":"0485205",
    "32420":"0485351",
    "11700":"0485309",
    "23540":"0485118",
    "19740":"0485143",
    "41900":"0485122",
    "18700":"0485326",
    "49340":"0485283",
    "14500":"0485257",
    "35980":"0485301",
    "18580":"0485268",
    "34900":"0485023",
    "46540":"0485306",
    "36140":"0485209",
    "27180":"0485338",
    "27740":"0485388",
    "25500":"0485006",
    "35100":"0485017",
    "20700":"0485044",
    "21340":"0485045",
    "25020":"0485354",
    "21500":"0485248",
    "41060":"0485298",
    "23420":"0485040",
    "20260":"0485377",
    "17420":"0485087",
    "19460":"0485310",
    "47300":"0485043",
    "33780":"0485395",
    "33700":"0485202",
    "16540":"0485303",
    "46340":"0485053",
    "20100":"0485008",
    "14740":"0485037",
    "24300":"0485213",
    "29700":"0485054",
    "43340":"0485249",
    "39660":"0485307",
    "15380":"0485324",
    "31540":"0485266",
    "10900":"0485085",
    "37460":"0485224",
    "13740":"0485201",
    "15680":"0485029",
    "13460":"0485340",
    "47220":"0485206",
    "39140":"0485345",
    "37340":"0485255",
    "31860":"0485392",
    "33540":"0485050",
    "34580":"0485028",
    "23460":"0485262",
    "42020":"0485361",
    "45940":"0485234",
    "41980":"0485323",
    "38300":"0485286",
    "40220":"0485019",
    "47900":"0485297",
    "49180":"0485140",
    "13900":"0485308",
    "29100":"0485031",
    "17780":"0485203",
    "41700":"0485032",
    "34980":"0485033",
    "40900":"0485251",
    "25980":"0485015",
    "10780":"0485012",
    "38220":"0485374",
    "11260":"0485373",
    "41420":"0485305",
    "28700":"0485363",
    "25220":"0485021",
    "13140":"0485339",
    "26820":"0485375",
    "45220":"0485004",
    "18880":"0485139",
    "11640":"0485083",
    "15540":"0485331",
    "25420":"0485281",
    "38900":"0485009",
    "41540":"0485016",
    "30460":"0485204",
    "30860":"0485381",
    "41180":"0485014",
    "39580":"0485020",
    "14260":"0485260",
    "45060":"0485035",
    "46220":"0485215",
    "19100":"0485007",
    "19820":"0485003",
    "17900":"0485120",
    "42200":"0485264",
    "19340":"0485295",
    "24220":"0485024",
    "17980":"0485284",
    "31080":"0485018",
    "38060":"0485353",
    "46140":"0485302",
    "31420":"0485254",
    "34100":"0485253",
    "34060":"0485034",
    "33340":"0485041",
    "18140":"0485226",
    "29180":"0485390",
    "30300":"0485296",
    "35380":"0485233",
    "41500":"0485259",
    "26620":"0485225",
    "44100":"0485282",
    "10540":"0485128",
    "38660":"0485138",
    "24580":"0485383",
    "46700":"0485379",
    "49020":"0485250",
    "27140":"0485258",
    "35300":"0485304",
    "21660":"0485022",
    "24500":"0485208",
    "42660":"0485207",
    "49420":"0485212",
    "11100":"0485355",
    "29340":"0485042",
    "14460":"0485387",
    "45300":"0485396",
    "40660":"0485142",
    "10420":"0485119",
    "27620":"0485132",
    "24020":"0485086",
    "24860":"0485382",
    "12020":"0485027",
    "25940":"0485048",
    "19300":"0485335",
    "13220":"0485210",
    "40380":"0485051",
    "44060":"0485013",
    "41940":"0485205",
    "22660":"0485351",
    "48900":"0485309",
    "13780":"0485118",
    "27980":"0485143",
    "29420":"0485122",
    "34820":"0485326",
    "31020":"0485283",
    "42100":"0485257",
    "29540":"0485301",
    "15180":"0485268",
    "13980":"0485023",
    "17140":"0485306",
    "16740":"0485209",
    "31340":"0485338",
    "30980":"0485388",
    "48060":"0485006",
    "12420":"0485017",
    "41620":"0485044",
    "44300":"0485045",
    "13380":"0485354",
    "26580":"0485248",
    "37980":"0485298",
    "49740":"0485040",
    "16700":"0485377",
    "13820":"0485087",
    "47460":"0485310",
    "30700":"0485043",
    "29620":"0485395",
    "18020":"0485202",
    "22020":"0485303",
    "12580":"0485053",
    "21780":"0485008",
    "16620":"0485037",
    "12700":"0485213",
    "28020":"0485054",
    "45780":"0485249",
    "26420":"0485307",
    "14100":"0485324",
    "46060":"0485266",
    "33260":"0485085",
    "19380":"0485224",
    "20220":"0485201",
    "14020":"0485029",
    "27500":"0485340",
    "29940":"0485206",
    "21140":"0485345",
    "38940":"0485255",
    "43100":"0485392",
    "22540":"0485050",
    "43780":"0485028",
    "12620":"0485262",
    "11540":"0485361",
    "16220":"0485234",
    "40980":"0485323",
    "13020":"0485286",
    "32900":"0485019",
    "39900":"0485297",
    "23900":"0485140",
    "21300":"0485308",
    "36780":"0485031",
    "41100":"0485203",
    "11180":"0485032",
    "12540":"0485033",
    "48140":"0485251",
    "26980":"0485015",
    "31700":"0485012",
    "22420":"0485374",
    "41660":"0485373",
    "12980":"0485305",
    "34620":"0485363",
    "19180":"0485021",
    "42140":"0485339",
    "48700":"0485375",
    "30140":"0485004",
    "34940":"0485139",
    "33220":"0485083",
    "11020":"0485331",
    "30620":"0485281",
    "36420":"0485009",
    "35620":"0485016",
    "14010":"0485204",
    "42680":"0485381",
    "34740":"0485014",
    "22520":"0485020",
    "39340":"0485260",
    "12220":"0485035",
    "19500":"0485215",
    "25260":"0485007",
    "49660":"0485003",
    "17660":"0485120",
    "30780":"0485264",
    "38860":"0485295",
    "16580":"0485024",
    "19780":"0485284",
    "33140":"0485018",
    "25620":"0485353",
    "29200":"0485302",
    "23060":"0485254",
    "30340":"0485253",
    "36740":"0485034",
    "43300":"0485041",
    "31180":"0485226",
    "27060":"0485390",
    "15260":"0485296",
    "15500":"0485233",
    "25540":"0485259",
    "33460":"0485225",
    "39380":"0485282",
    "26300":"0485128",
    "47940":"0485138",
    "32780":"0485383",
    "33100":"0485379",
    "47380":"0485250",
    "32820":"0485258",
    "24660":"0485304",
    "26900":"0485022",
    "42700":"0485208",
    "27900":"0485207",
    "11500":"0485212",
    "16860":"0485355",
    "28940":"0485042",
    "22220":"0485387",
    "22180":"0485396",
    "24340":"0485142",
    "39820":"0485119",
    "10740":"0485132",
    "49620":"0485086",
    "24420":"0485382",
    "46660":"0485027",
    "29460":"0485048",
    "40580":"0485335",
    "29020":"0485210",
    "14860":"0485051",
    "29740":"0485013",
    "19060":"0485205",
    "31140":"0485351",
    "36260":"0485309",
    "10500":"0485118",
    "29820":"0485143",
    "32580":"0485122",
    "41860":"0485326",
    "10380":"0485283",
    "48300":"0485257",
    "14540":"0485301",
    "26380":"0485268",
    "16020":"0485023",
    "48660":"0485306",
    "26140":"0485209",
    "27260":"0485338",
    "47580":"0485388",
    "42340":"0485006",
    "21060":"0485017",
    "12100":"0485044",
    "21820":"0485045",
    "20020":"0485354",
    "31460":"0485248",
    "44700":"0485298",
    "17020":"0485040",
    "41140":"0485377",
    "28740":"0485087",
    "28140":"0485310",
    "43580":"0485043",
    "10580":"0485395",
    "48620":"0485202",
    "39460":"0485303",
    "36540":"0485053",
    "46520":"0485008",
    "45820":"0485037",
    "22500":"0485213",
    "47020":"0485054",
    "36980":"0485249",
    "28420":"0485307",
    "36500":"0485324",
    "43900":"0485266",
    "17300":"0485085",
    "37860":"0485224",
    "16060":"0485201",
    "28660":"0485029",
    "44180":"0485340",
    "37900":"0485206",
    "16300":"0485345",
    "43420":"0485255",
    "10180":"0485392",
    "35840":"0485050",
    "27780":"0485028",
    "16940":"0485262",
    "24140":"0485361",
    "30020":"0485234",
    "15940":"0485323",
    "24260":"0485286",
    "48260":"0485019",
    "35660":"0485297",
    "40420":"0485140",
    "24540":"0485308",
    "19140":"0485031",
    "39740":"0485203",
    "39540":"0485032",
    "27340":"0485033",
    "17820":"0485251",
    "27860":"0485015",
    "38340":"0485012",
    "38540":"0485374",
    "42220":"0485373",
    "33860":"0485305",
    "25180":"0485363",
    "36100":"0485021",
    "49700":"0485339",
    "15980":"0485375",
    "20940":"0485004",
    "47260":"0485139",
    "25860":"0485083",
    "19660":"0485331",
    "40340":"0485281",
    "31740":"0485009",
    "16820":"0485016",
    "37100":"0485204",
    "41740":"0485381",
    "45460":"0485014",
    "45540":"0485020",
    "40140":"0485260",
    "42540":"0485035",
    "16980":"0485215",
    "37620":"0485007",
    "44940":"0485003",
    "22140":"0485120",
    "36220":"0485264",
    "44420":"0485295",
    "24780":"0485024",
    "25060":"0485284",
    "33660":"0485018",
    "22380":"0485353",
    "12940":"0485302",
    "17860":"0485254",
    "44140":"0485253",
    "48540":"0485034",
    "27100":"0485041",
    "31900":"0485226",
    "39300":"0485390",
    "16180":"0485296",
    "28100":"0485233",
    "20740":"0485259",
    "11460":"0485225",
    "23580":"0485282",
    "44220":"0485128"
}

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

            val = []
            for z in zcta_occ_loss_complete:
                val.append(z["display"])

            msa_l = list(t.keys())
            zcta_occ_loss_complete = []
            i = 0
            for msa in msa_l:
                d = val[i]
                zcta_occ_loss_complete.append({
                    "msa_id" : msa,
                    "display" : d
                })
                i += 1
                if i >= len(val):
                    i = 0

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

            val = []
            for z in zcta_ind_loss_complete:
                val.append(z["display"])

            msa_l = list(t.keys())
            zcta_ind_loss_complete = []
            i = 0
            for msa in msa_l:
                d = val[i]
                zcta_ind_loss_complete.append({
                    "msa_id": msa,
                    "display": d
                })
                i += 1
                if i >= len(val):
                    i = 0

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

            val = []
            for z in zcta_ind_loss_complete:
                val.append(z["display"])

            msa_l = list(t.keys())
            zcta_ind_loss_complete = []
            i = 0
            for msa in msa_l:
                d = val[i]
                zcta_ind_loss_complete.append({
                    "msa_id": msa,
                    "display": d
                })
                i += 1
                if i >= len(val):
                    i = 0

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

@main.route('/get_ind_heir_data')
def get_ind_heir_data():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute('SELECT * FROM _metro_employment_tool_tables.ind_hier_viz_data')

    data = cur.fetchone()

    return jsonify(data)

if __name__ == '__main__':
    pass