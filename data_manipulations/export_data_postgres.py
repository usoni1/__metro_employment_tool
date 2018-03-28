import psycopg2
import csv
import pandas
from treelib import Tree
import re
import json
from data_manipulations import util

def store_occ_distributions_MSA():
    conn = util.get_connection()
    f = open('./raw_data/MSA_M2016_dl.csv', 'r')
    reader = csv.reader(f, delimiter=',')

    level_correction = {
        "major" : "Major",
        "minor" : "Minor",
        "detailed" : "Detailed",
        "broad" : "Broad",
        "total" : "Special"
    }

    sql = ''
    flag1 = True
    for row in reader:
        if(flag1):
            flag1 = False
            continue
        sql += '(\'%s\',\'%s\',\'%s\',%d,%s)' % (row[1], row[3], level_correction[row[5]], int(row[6].replace(',', '').replace('**', '-1')), 'false')
        sql += ','

    f = open('./raw_data/aMSA_M2016_dl.csv', 'r')
    reader = csv.reader(f, delimiter=',')

    flag1 = True
    for row in reader:
        if (flag1):
            flag1 = False
            continue
        sql += '(\'%s\',\'%s\',\'%s\',%d,%s)' % (row[1], row[3], level_correction[row[5]], int(row[6].replace(',', '').replace('**', '-1')), 'false')
        sql += ','

    print("SQL statement created \n first few bits of SQL: ")
    print(sql[:100])

    cur = conn.cursor()
    cur.execute("TRUNCATE _metro_employment_tool_tables.\"BLS_OES_2016\"")
    cur.execute("INSERT INTO _metro_employment_tool_tables.\"BLS_OES_2016\""
                " VALUES " + sql[:-1] )

    print("Values inserted")

    commit_go_ahead = input("Go ahead with commit...Y/N...\n")

    if(commit_go_ahead == 'Y'):
        conn.commit()
    cur.close()

def store_occ_distribution_ZCTA():
    conn = util.get_connection()
    file_paths = {
        "Major" : './raw_data/soc_major_sums.csv',
        "Minor" : './raw_data/soc_minor_sums.csv',
        "Broad" : './raw_data/soc_broad_sums.csv',
        "Detailed" : './raw_data/soc_detail_sums.csv'
    }
    suffix = {
        "Major": '-0000',
        "Minor": '000',
        "Broad": '0',
        "Detailed": ''
    }

    sql = ''
    for level, path in file_paths.items():
        csv = pandas.read_csv(path, sep=',')
        for index, row in csv.iterrows():
            ZCTA_ID = row['ZCTA_GEOID10']
            if(row.isnull()['ZCTA_GEOID10'] != True):
                for col in csv.columns.values[1:]:
                    sql += '(\'%s\',\'%s\',\'%s\',%d, %s)' % (col+suffix[level], level, str(int(ZCTA_ID)), int(round(row[col])), 'false')
                    sql += ','

    print("SQL statement created \n first few bits of SQL: ")
    print(sql[:100])

    cur = conn.cursor()
    cur.execute("TRUNCATE _metro_employment_tool_tables.\"ZCTA_OCC_COUNTS\"")
    cur.execute("INSERT INTO _metro_employment_tool_tables.\"ZCTA_OCC_COUNTS\""
                " VALUES " + sql[:-1])

    print("All Values inserted")

    commit_go_ahead = input("Go ahead with commit...Y/N...\n")

    if (commit_go_ahead == 'Y'):
        conn.commit()
    cur.close()

def store_onet_dataset(conn):
    csv = pandas.read_csv('./raw_data/skills.csv', sep=',')
    sql =''
    for index, row in csv.iterrows():
        sql += '(\'%s\',\'%s\',\'%s\', %f)' % (str(row['O*NET-SOC Code']), row['Element ID'], row['Scale ID'], row['Data Value'])
        sql += ','

    print("SQL statement created \n first few bits of SQL: ")
    print(sql[:100])

    cur = conn.cursor()
    cur.execute("TRUNCATE _metro_employment_tool_tables.\"ONET_SKILLS\"")
    cur.execute("INSERT INTO _metro_employment_tool_tables.\"ONET_SKILLS\""
                " VALUES " + sql[:-1])

    print("Values inserted")

    commit_go_ahead = input("Go ahead with commit...Y/N...\n")

    if (commit_go_ahead == 'Y'):
        conn.commit()
    cur.close()

def store_occuption_list_and_heirarchy(conn, db_store=False, file_path = './raw_data/soc_structure_2018.xlsx', external_add_occs = None):
    reader = pandas.read_excel(file_path)
    # fill all the separate occupations
    major_occ_list = []
    minor_occ_list = []
    broad_occ_list = []
    detailed_occ_list = []
    for index, row in reader.iterrows():
        if (row.notnull()['Major Group']):
            major_occ_list.append(row['Major Group'])
        elif (row.notnull()['Minor Group']):
            minor_occ_list.append(row['Minor Group'])
        elif (row.notnull()['Broad Group']):
            broad_occ_list.append(row['Broad Group'])
        elif (row.notnull()['Detailed Occupation']):
            detailed_occ_list.append(row['Detailed Occupation'])
        else:
            print('Invalid tuple')

    print("All occupations level list generated from file")

    if external_add_occs is not None:
        major_occ_list = list(set(major_occ_list).union(set(external_add_occs["Major"])))
        minor_occ_list = list(set(minor_occ_list).union(set(external_add_occs["Minor"])))
        broad_occ_list = list(set(broad_occ_list).union(set(external_add_occs["Broad"])))
        detailed_occ_list = list(set(detailed_occ_list).union(set(external_add_occs["Detailed"])))

    print("added external occupations")

    #generate the tree heirarchy
    tree = Tree()
    tree.create_node("Occupations", "Occupations")

    #create Major to Minor Connections
    for major_occ in major_occ_list:
        tree.create_node(major_occ, major_occ, "Occupations")
        major_occ_prefix = major_occ[:2]
        r = re.compile(major_occ_prefix + '.*')
        matched_minor_occ = [minor_occ for minor_occ in minor_occ_list if r.match(minor_occ)]
        for matched_occ in matched_minor_occ:
            tree.create_node(matched_occ, matched_occ, major_occ)

    print("Major->Minor Done")

    #create minor to broad connections
    for minor_occ in minor_occ_list:
        minor_occ_prefix = minor_occ[:4]
        r = re.compile(minor_occ_prefix + '.*')
        matched_broad_occ = [broad_occ for broad_occ in broad_occ_list if r.match(broad_occ)]
        for matched_occ in matched_broad_occ:
            tree.create_node(matched_occ, matched_occ, minor_occ)

    print("Minor->Broad Done")

    #create broad to detailed connections
    for broad_occ in broad_occ_list:
        broad_occ_prefix = broad_occ[:6]
        r = re.compile(broad_occ_prefix + '.*')
        matched_detailed_occ = [detailed_occ for detailed_occ in detailed_occ_list if r.match(detailed_occ)]
        for matched_occ in matched_detailed_occ:
            tree.create_node(matched_occ, matched_occ, broad_occ)

    print("Broad->Detailed")

    print("occ hierarchy created")
    if(db_store):
        cur = conn.cursor()
        cur.execute('INSERT INTO '
                    '_metro_employment_tool._metro_employment_tool_tables."OCC_HIERARHCY" '
                    'VALUES (\'%s\')' % (tree.to_json()))
        conn.commit()
        cur.close()
        print("occ hierarchy stored")
    return (tree, major_occ_list, minor_occ_list, broad_occ_list, detailed_occ_list)

def create_bls_occ_csv(tree, conn):
    #todo tree should be created via the database
    cur = conn.cursor()
    #filling the occ for each msa bottom up, detailed -> major

if __name__ == '__main__':
   store_occ_distributions_MSA()
