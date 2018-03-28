import psycopg2
import pandas
import csv
import codecs
import numpy as np

def generate_MSA_skills(conn):
    #fetch all the avaiable skills
    cur = conn.cursor()
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
                    '"OCC_GROUP" =\'detailed\' and "MSA_CODE" = \'%s\' and "TOT_EMP" != -1' % (msa) )
        msa_skill_list_temp = [list(msa_tuple) for msa_tuple in cur.fetchall()]
        tot_occ_count = 0
        #todo shift tot_occ_count down as it needs to get reinitialized
        for skill in skill_list:
            final_skill_value_LV = 0
            final_skill_value_IM = 0
            msa_tuple_LV = [msa]
            msa_tuple_IM = [msa]
            for msa_tuple in msa_skill_list_temp:
                if(msa_tuple[1] + '.00' in onet_skill_set):
                    tot_occ_count += msa_tuple[2]
                    #for level
                    skill_value_LV = onet_skill_set[msa_tuple[1] + '.00'][skill]['LV']
                    final_skill_value_LV += (msa_tuple[2] * skill_value_LV)

                    #for importance
                    skill_value_IM = onet_skill_set[msa_tuple[1] + '.00'][skill]['IM']
                    final_skill_value_IM += (msa_tuple[2] * skill_value_IM)

            msa_tuple_IM.extend([skill, final_skill_value_IM/tot_occ_count, 'IM'])
            msa_tuple_LV.extend([skill, final_skill_value_LV/tot_occ_count, 'LV'])
            msa_skill_list.extend([msa_tuple_IM, msa_tuple_LV])
        print("skill value generated for MSA %s" % (msa))


def generate_ZCTA_skills_count(conn):
    pass

def generate_MSA_losses(conn):
    # reader = csv.reader(codecs.open('./raw_data/soc_structure_2018.csv', 'r', 'utf-16'), delimiter=',')
    pass

if __name__ == '__main__':
    hostname = 'localhost'
    username = 'metro_insight_admin'
    password = 'password'
    database = '_metro_employment_tool'

    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=5433)

    generate_MSA_losses(conn)