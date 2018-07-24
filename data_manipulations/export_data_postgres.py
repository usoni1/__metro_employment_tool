import csv
import pandas
from treelib import Tree
import re
from data_manipulations import util
import math
import json

def store_occ_distributions_MSA():
    conn = util.get_connection()
    f = open('./data/raw_data/MSA_M2016_dl.csv', 'r')
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

    f = open('./data/raw_data/aMSA_M2016_dl.csv', 'r')
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

    print("Values inserted for BLS_OES_2016")

    conn.commit()
    cur.close()

def store_occ_distribution_ZCTA():
    conn = util.get_connection()
    file_paths = {
        "Major" : './data/raw_data/soc_major_sums.csv',
        "Minor" : './data/raw_data/soc_minor_sums.csv',
        "Broad" : './data/raw_data/soc_broad_sums.csv',
        "Detailed" : './data/raw_data/soc_detail_sums.csv'
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

    print("All Values inserted for ZCTA_OCC_COUNTS")

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

def store_occuption_list_and_heirarchy(conn, db_store=False, file_path = './data/raw_data/soc_structure_2018.xlsx', verbose = True):
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

    if verbose:
        print("All occupations level list generated from file")

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

    if verbose:
        print("Major->Minor Done")

    #create minor to broad connections
    for minor_occ in minor_occ_list:
        minor_occ_prefix = minor_occ[:4]
        r = re.compile(minor_occ_prefix + '.*')
        matched_broad_occ = [broad_occ for broad_occ in broad_occ_list if r.match(broad_occ)]
        for matched_occ in matched_broad_occ:
            tree.create_node(matched_occ, matched_occ, minor_occ)

    if verbose:
        print("Minor->Broad Done")

    #create broad to detailed connections
    for broad_occ in broad_occ_list:
        broad_occ_prefix = broad_occ[:6]
        r = re.compile(broad_occ_prefix + '.*')
        matched_detailed_occ = [detailed_occ for detailed_occ in detailed_occ_list if r.match(detailed_occ)]
        for matched_occ in matched_detailed_occ:
            tree.create_node(matched_occ, matched_occ, broad_occ)

    if verbose:
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

def store_industry_list_and_heirarchy(db_store=False, file_path = './data/raw_data/NAICS 2-6 digit_2017_Codes.xlsx', verbose = True):
    conn = util.get_connection()
    reader = pandas.read_excel(file_path)

    sector_list = []
    subsector_list = []
    ind_group_list = []
    NAICS_group_list = []
    national_industry_list = []

    for index, row in reader.iterrows():
        naics_code = row["2017 NAICS US   Code"]
        naics_name = row["2017 NAICS US Title"]

        if isinstance(naics_code, float) and math.isnan(naics_code):
            continue

        naics_code = str(naics_code)

        if naics_code == "31-33":
            sector_list.append(("31", "Manufacturing"))
            sector_list.append(("32", "Manufacturing"))
            sector_list.append(("33", "Manufacturing"))
            continue

        if naics_code == "44-45":
            sector_list.append(("44", "Retail Trade"))
            sector_list.append(("45", "Retail Trade"))
            continue

        if naics_code == "48-49":
            sector_list.append(("48", "Transportation and Warehousing"))
            sector_list.append(("49", "Transportation and Warehousing"))
            continue

        if len(naics_code) == 2:
            sector_list.append(((naics_code, naics_name)))
        elif len(naics_code) == 3:
            subsector_list.append(((naics_code, naics_name)))
        elif len(naics_code) == 4:
            ind_group_list.append(((naics_code, naics_name)))
        elif len(naics_code) == 5:
            NAICS_group_list.append(((naics_code, naics_name)))
        elif len(naics_code) == 6:
            national_industry_list.append(((naics_code, naics_name)))
        else:
            print("invalid code %s" % str(naics_code))

    if verbose:
        print("All levels industry list generated")

    # generate the tree heirarchy
    tree = Tree()
    tree.create_node("Industries", "Industries")

    connections = [("sector->subsector", sector_list, subsector_list),
                   ("subsector->ind_group", subsector_list, ind_group_list),
                   ("ind_group->NAICS_group", ind_group_list, NAICS_group_list),
                   ("NAICS_group->national_industry", NAICS_group_list, national_industry_list)]

    for idx, connection in enumerate(connections):
        level = connection[0]
        t1 = connection[1] # eg sector_list
        t2 = connection[2] # eg subsector_list

        for _t1 in t1: #_t1 eg just a sector
            if idx == 0:
                # as sector comes under root Industries node
                tree.create_node(_t1[0], _t1[0], "Industries", _t1[1])
            r = re.compile(_t1[0] + '.')
            matched_t2 = [t3[0] for t3 in t2 if r.match(t3[0])]
            for _matched_t2 in matched_t2:
                tree.create_node(_matched_t2, _matched_t2, _t1[0])

        if verbose:
            print(level + " done.")
            print(tree)



    if (db_store):
        cur = conn.cursor()
        cur.execute('INSERT INTO '
                    '_metro_employment_tool._metro_employment_tool_tables."ind_hierarchy" '
                    'VALUES (\'%s\')' % (tree.to_json(with_data=True)))
        conn.commit()
        cur.close()
        print("occ hierarchy stored")

    return (tree, sector_list, subsector_list, ind_group_list, NAICS_group_list, national_industry_list)

def create_bls_occ_csv(tree, conn):
    #todo tree should be created via the database
    cur = conn.cursor()
    #filling the occ for each msa bottom up, detailed -> major

def clean_up_db_occ():
    """
    retains only occupation code present in soc_structure_2018

    :return:
    """
    #todo major use the crosswalk and map instead of simply removing the DBs
    conn = util.get_connection()

    [tree, major_list, minor_list, broad_list, detailed_list] = store_occuption_list_and_heirarchy(conn, False, verbose = False)
    combined_list = []
    combined_list.extend([*major_list, *minor_list, *broad_list, *detailed_list])

    tables = ["BLS_NEM_2016", "BLS_OES_2016", "ZCTA_OCC_COUNTS"]
    for table in tables:
        #cleaning up BLS_NEM_2016
        #first fetch all occupation codes there are
        cur = conn.cursor()
        cur.execute('SELECT DISTINCT("OCC_CODE") '
                    'FROM _metro_employment_tool_tables."%s"' % table)
        combined_list_db = [row[0] for row in cur.fetchall()]

        # occupations present in the database but not in soc_structure_2018
        to_remove_occ_codes = list(set(combined_list_db) - set(combined_list))
        cur.execute('SELECT COUNT(*)'
                    'FROM _metro_employment_tool_tables."%s"' % table)
        before_removing_count = cur.fetchone()[0]

        sql = 'DELETE FROM _metro_employment_tool_tables."%s" WHERE ' % table

        if len(to_remove_occ_codes) == 0:
            print("already deleted for table %s" % table)
            continue

        for occ_code in to_remove_occ_codes[:-1]:
            sql += '"OCC_CODE" = \'%s\' OR ' % occ_code
        sql += '"OCC_CODE" = \'%s\'' % to_remove_occ_codes[-1]


        cur.execute(sql)
        conn.commit()

        cur.execute('SELECT COUNT(*)'
                    'FROM _metro_employment_tool_tables."%s"' % table)

        after_removing_count = cur.fetchone()[0]

        print("before removing %d from table %s" % (before_removing_count, table))
        print("after removing %d after table %s" % (after_removing_count, table))

def get_final_tree(final_tree, final_tree_current_level, node, tree, cur):
    """
    complementary recursive function for create_industry_heirarchy_for_viz
    :return:
    """
    children_nodes = tree.children(node)
    for child in children_nodes:
        child_tag = child.tag

        if child_tag in ('31', '32', '33'):
            ind_code = '31-330'
        elif child_tag in ('44', '45'):
            ind_code = '44-450'
        elif child_tag in ('48', '49'):
            ind_code = '48-490'
        else:
            ind_code = child_tag + (6-len(child_tag))*'0'

        cur.execute("select skill_info -> 'skill_data' as skill_list "
                    "from _metro_employment_tool_tables.ind_skill_data "
                    "where skill_info->>'level' = 'LV' and ind='%s'" % ind_code)

        t2 = {}
        for skill_info in cur.fetchall():
            t2[skill_info[0]["skill"]] = skill_info[0]["value"]

        t1_child = {
            "data" : [
                child.data,
                False,
                0,
                t2
            ],
            "name" : child_tag,
            "children" : []
        }
        final_tree_current_level["children"].append(t1_child)
        get_final_tree(final_tree, t1_child, child_tag, tree, cur)

def create_industry_heirarchy_for_viz(db_store=False, verbose = True):
    """
    creates final industry hierarchy data structure to be used for Visualization
    :param db_store:
    :return:
    """
    final_tree = {
        "name" : "root",
        "data" : ["Industries", ],
        "children" : []
    }

    conn = util.get_connection()
    cur = conn.cursor()

    ind_tree = store_industry_list_and_heirarchy(verbose=False)[0]
    get_final_tree(final_tree, final_tree, "Industries", ind_tree, cur)

    json.dump(final_tree, open("flare1.json", 'w'), indent=4, separators=(',', ':'))

if __name__ == '__main__':
   # store_occ_distributions_MSA()
   #  store_industry_list_and_heirarchy(db_store=True)
   create_industry_heirarchy_for_viz()