import psycopg2
import pandas
import csv
import codecs
import numpy as np
import json
import pprint as pp

def generate_MSA_skills(conn):
    #fetch all the avaiable skills


    cur = conn.cursor()

    cur.execute('delete from _metro_employment_tool_tables.msa_skill_data')

    cur.execute('SELECT DISTINCT(\"SKILL_ID\") from '
                '_metro_employment_tool._metro_employment_tool_tables.\"ONET_SKILLS\"')
    skill_list = [skill[0] for skill in cur.fetchall()]

    #fetch all the avaiable MSAs
    cur.execute('SELECT DISTINCT ("MSA_CODE") from '
                '_metro_employment_tool._metro_employment_tool_tables."BLS_OES_2016"')
    MSA_list = [msa[0] for msa in cur.fetchall()]

    cur = conn.cursor()
    cur.execute('SELECT * FROM '
                '_metro_employment_tool._metro_employment_tool_tables."ONET_SKILLS" '
                'WHERE "ONET_SOC_CODE" ~ \'.*\.00\'')


    # conn.commit()

    onet_skill_set = {}
    for skill_tuple in cur.fetchall():
        onet_soc_code = skill_tuple[0]
        skill_id = skill_tuple[1]
        scale = skill_tuple[2]
        value = skill_tuple[3]
        if(onet_soc_code in onet_skill_set):
            if(skill_id in onet_skill_set[onet_soc_code]):
                onet_skill_set[onet_soc_code][skill_id][scale] = value
            else:
                onet_skill_set[onet_soc_code][skill_id] = {}
                onet_skill_set[onet_soc_code][skill_id][scale] = value
        else:
            onet_skill_set[onet_soc_code] = {}
            onet_skill_set[onet_soc_code][skill_id] = {}
            onet_skill_set[onet_soc_code][skill_id][scale] = value

    msa_skill_list = []
    for msa in MSA_list:
        cur.execute('SELECT "MSA_CODE", "OCC_CODE", "TOT_EMP" from '
                    '_metro_employment_tool._metro_employment_tool_tables."BLS_OES_2016" '
                    'where '
                    '"OCC_GROUP" =\'Detailed\' and "MSA_CODE" = \'%s\' and "TOT_EMP" != -1' % (msa) )
        msa_skill_list_temp = [list(msa_tuple) for msa_tuple in cur.fetchall()]


        #todo shift tot_occ_count down as it needs to get reinitialized
        for skill in skill_list:
            tot_occ_count = 0
            final_skill_value_LV = 0
            final_skill_value_IM = 0
            msa_tuple_LV = [msa]
            msa_tuple_IM = [msa]
            msa_skill_info_LV = { "level" : "LV", "skill_data" : {}}
            msa_skill_info_IM = {"level": "IM", "skill_data": {}}

            for msa_tuple in msa_skill_list_temp:
                if(msa_tuple[1] + '.00' in onet_skill_set):
                    tot_occ_count += msa_tuple[2]
                    #for level
                    skill_value_LV = onet_skill_set[msa_tuple[1] + '.00'][skill]['LV']
                    final_skill_value_LV += (msa_tuple[2] * skill_value_LV)

                    #for importance
                    skill_value_IM = onet_skill_set[msa_tuple[1] + '.00'][skill]['IM']
                    final_skill_value_IM += (msa_tuple[2] * skill_value_IM)

            msa_skill_info_LV["skill_data"]["skill"] = skill
            msa_skill_info_LV["skill_data"]["value"] = final_skill_value_LV/tot_occ_count

            msa_skill_info_IM["skill_data"]["skill"] = skill
            msa_skill_info_IM["skill_data"][skill] = final_skill_value_IM/tot_occ_count

            cur.execute("INSERT INTO _metro_employment_tool_tables.msa_skill_data "
                        "VALUES "
                        "(%d, '%s')" % (int(msa), json.dumps(msa_skill_info_LV)))

            cur.execute("INSERT INTO _metro_employment_tool_tables.msa_skill_data "
                        "VALUES "
                        "(%d, '%s')" % (int(msa), json.dumps(msa_skill_info_IM)))

            msa_tuple_IM.extend([skill, final_skill_value_IM/tot_occ_count, 'IM'])
            msa_tuple_LV.extend([skill, final_skill_value_LV/tot_occ_count, 'LV'])
            msa_skill_list.extend([msa_tuple_IM, msa_tuple_LV])

        conn.commit()
        print("skill value generated for MSA %s" % (msa))

def generate_ZCTA_skills_count(conn):
    #fetch all the avaiable skills


    cur = conn.cursor()

    cur.execute('delete from _metro_employment_tool_tables.zcta_skill_data')

    cur.execute('SELECT DISTINCT(\"SKILL_ID\") from '
                '_metro_employment_tool._metro_employment_tool_tables.\"ONET_SKILLS\"')
    skill_list = [skill[0] for skill in cur.fetchall()]

    #fetch all the avaiable MSAs
    cur.execute('SELECT DISTINCT ("ZCTA_ID") from '
                '_metro_employment_tool._metro_employment_tool_tables."ZCTA_OCC_COUNTS"')
    zcta_list = [zcta[0] for zcta in cur.fetchall()]

    cur = conn.cursor()
    cur.execute('SELECT * FROM '
                '_metro_employment_tool._metro_employment_tool_tables."ONET_SKILLS" '
                'WHERE "ONET_SOC_CODE" ~ \'.*\.00\'')


    # conn.commit()

    onet_skill_set = {}
    for skill_tuple in cur.fetchall():
        onet_soc_code = skill_tuple[0]
        skill_id = skill_tuple[1]
        scale = skill_tuple[2]
        value = skill_tuple[3]
        if(onet_soc_code in onet_skill_set):
            if(skill_id in onet_skill_set[onet_soc_code]):
                onet_skill_set[onet_soc_code][skill_id][scale] = value
            else:
                onet_skill_set[onet_soc_code][skill_id] = {}
                onet_skill_set[onet_soc_code][skill_id][scale] = value
        else:
            onet_skill_set[onet_soc_code] = {}
            onet_skill_set[onet_soc_code][skill_id] = {}
            onet_skill_set[onet_soc_code][skill_id][scale] = value

    zcta_skill_list = []
    for zcta in zcta_list:
        cur.execute('SELECT "ZCTA_ID", "OCC_CODE", "TOT_EMP" from '
                    '_metro_employment_tool._metro_employment_tool_tables."ZCTA_OCC_COUNTS" '
                    'where '
                    '"OCC_GROUP" =\'Detailed\' and "ZCTA_ID" = \'%s\' and "TOT_EMP" != -1' % (zcta) )
        zcta_skill_list_temp = [list(zcta_tuple) for zcta_tuple in cur.fetchall()]


        #todo shift tot_occ_count down as it needs to get reinitialized
        for skill in skill_list:
            tot_occ_count = 0
            final_skill_value_LV = 0
            final_skill_value_IM = 0
            zcta_tuple_LV = [zcta]
            zcta_tuple_IM = [zcta]
            zcta_skill_info_LV = { "level" : "LV", "skill_data" : {}}
            zcta_skill_info_IM = {"level": "IM", "skill_data": {}}

            for zcta_tuple in zcta_skill_list_temp:
                if(zcta_tuple[1] + '.00' in onet_skill_set):
                    tot_occ_count += zcta_tuple[2]
                    #for level
                    skill_value_LV = onet_skill_set[zcta_tuple[1] + '.00'][skill]['LV']
                    final_skill_value_LV += (zcta_tuple[2] * skill_value_LV)

                    #for importance
                    skill_value_IM = onet_skill_set[zcta_tuple[1] + '.00'][skill]['IM']
                    final_skill_value_IM += (zcta_tuple[2] * skill_value_IM)

            if(tot_occ_count != 0):
                zcta_skill_info_LV["skill_data"]["skill"] = skill
                zcta_skill_info_LV["skill_data"]["value"] = final_skill_value_LV/tot_occ_count

                zcta_skill_info_IM["skill_data"]["skill"] = skill
                zcta_skill_info_IM["skill_data"][skill] = final_skill_value_IM/tot_occ_count
            else:
                zcta_skill_info_LV["skill_data"]["skill"] = skill
                zcta_skill_info_LV["skill_data"]["value"] = -1

                zcta_skill_info_IM["skill_data"]["skill"] = skill
                zcta_skill_info_IM["skill_data"][skill] = -1

            cur.execute("INSERT INTO _metro_employment_tool_tables.zcta_skill_data "
                        "VALUES "
                        "(%d, '%s')" % (int(zcta), json.dumps(zcta_skill_info_LV)))

            cur.execute("INSERT INTO _metro_employment_tool_tables.msa_skill_data "
                        "VALUES "
                        "(%d, '%s')" % (int(zcta), json.dumps(zcta_skill_info_IM)))


        conn.commit()
        print("skill value generated for ZCTA %s" % (zcta))

def generate_MSA_losses(conn):
    # reader = csv.reader(codecs.open('./raw_data/soc_structure_2018.csv', 'r', 'utf-16'), delimiter=',')
    pass

if __name__ == '__main__':
    hostname = 'localhost'
    username = 'metro_insight_admin'
    password = 'password'
    database = '_metro_employment_tool'

    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=5433)

    generate_ZCTA_skills_count(conn)