from data_manipulations import export_data_postgres as edp, \
    util, \
    get_latest_bls_nem as bls_funcs
from treelib import Tree
import numpy as np
import pandas as pd
import copy

def aggregate_occ(table_name, unknown_count_default):
    #do not run after you have run aggregate_ind(), if needed run get_latest_bls_nem then this function, then aggregate_ind()
    conn = util.get_connection()


    if(table_name == 'BLS_NEM_2016'):
        unit = "IND_CODE"
    elif(table_name == 'ZCTA_OCC_COUNTS'):
        unit = "ZCTA_ID"
    elif(table_name == 'BLS_OES_2016'):
        unit = "MSA_CODE"
    else:
        print("can't handle this table")

    #fetch industry data from the server industry wise
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT "%s" '
                'from _metro_employment_tool._metro_employment_tool_tables."%s" '
                'ORDER BY "%s";' % (unit, table_name, unit) )
    unit_code_list = [unit_code for unit_code in cur.fetchall()]
    #do for every industry add occs to major so that they get broadcaseted accross everywhere
    # cur.execute('SELECT DISTINCT "OCC_CODE" from _metro_employment_tool_tables."BLS_NEM_2016"';)

    # here we update the tree by putting occupations that are present in BLS_NEM_2016, or BLS_OES_2016, or ZCTA_OCC_COUNTS
    # in the correct position in the tree. This way we make sure that for any unit, the occupation vector would be same
    # for sure

    levels = ["Major", "Minor", "Broad", "Detailed"]

    (tree, major_list, minor_list, broad_list, detailed_list) = edp.store_occuption_list_and_heirarchy(conn, False)


    top_list_map = {"Major": major_list, "Minor": minor_list, "Broad": broad_list, "Detailed": detailed_list}

    for unit_code in unit_code_list:
        unit_code = unit_code[0]
        cur.execute('SELECT * '
                         'from _metro_employment_tool._metro_employment_tool_tables."%s" '
                         'where "%s" = \'%s\'' % (table_name, unit, unit_code))

        #iterate over the rows and make neccessary data structure for fast processing
        #todo check to see if removing occ_list and putting it in different variable reduces overall time
        fa_unit_data = {
            "Major": {
                "occ_list" : [],
                "remaining_occ" : None
            },
            "Minor" : {
                "occ_list" : [],
                "remaining_occ": None
            },
            "Broad" : {
                "occ_list" : [],
                "remaining_occ": None
            },
            "Detailed": {
                "occ_list" : [],
                "remaining_occ": None
            },
            "Special": {
                "occ_list" : [],
                "remaining_occ": None
            }
        }

        for row in cur.fetchall():
            if(table_name == 'BLS_NEM_2016'):
                occ_level = row[3]
                occ_code = row[2]
                occ_count = row[4]
                fa_unit_data[occ_level][occ_code] = occ_count
                fa_unit_data[occ_level]['occ_list'].append(occ_code)
            elif(table_name == 'ZCTA_OCC_COUNTS'):
                occ_level = row[1]
                occ_code = row[0]
                occ_count = row[4]
                fa_unit_data[occ_level][occ_code] = occ_count
                fa_unit_data[occ_level]['occ_list'].append(occ_code)
            elif(table_name == 'BLS_OES_2016'):
                occ_level = row[2]
                occ_code = row[1]
                occ_count = row[3]
                fa_unit_data[occ_level][occ_code] = occ_count
                fa_unit_data[occ_level]['occ_list'].append(occ_code)
            else:
                print("unknown table")



        #do set subtraction operation at each level, to find out the holes(occ that need to be filled with value)
        for level in levels:
            fa_unit_data[level]["remaining_occ"] = list(set(top_list_map[level]).difference(set(fa_unit_data[level]["occ_list"])))

        #create level tree for shorting the code
        level_tree = Tree()
        level_tree.create_node("Major", "Major")
        level_tree.create_node("Minor", "Minor", parent="Major")
        level_tree.create_node("Broad", "Broad", parent="Minor")
        level_tree.create_node("Detailed", "Detailed", parent="Broad")
        sql = ''
        for level in reversed(levels):
            #update the main dictionary and at the same time make the required SQL insert statements
            req_level = fa_unit_data[level]
            req_child_level = fa_unit_data[level_tree.children(level)[0].tag] if level != 'Detailed' else None
            req_remaining_occ = req_level["remaining_occ"]
            for remaining_occ in req_remaining_occ:
                if req_child_level:
                    #i.e. level is not detailed
                    lower_level_occ = tree.children(remaining_occ)
                    req_aggregated_count = 0
                    for l_occ in lower_level_occ:
                        if(req_child_level[l_occ.tag] == -1):
                            req_aggregated_count += 0
                        else:
                            req_aggregated_count += req_child_level[l_occ.tag]
                else:
                    req_aggregated_count = unknown_count_default

                req_level[remaining_occ] = req_aggregated_count
                if(table_name == 'BLS_NEM_2016'):
                    sql += '(\'%s\',\'%s\',\'%s\',\'%s\',%d, %s)' \
                           % (
                               unit_code,
                               bls_funcs.find_ind_level(unit_code),
                               remaining_occ,
                               bls_funcs.find_occ_level(remaining_occ),
                               req_aggregated_count,
                               'true')
                elif(table_name == 'ZCTA_OCC_COUNTS'):
                    sql += '(\'%s\', \'%s\', \'%s\', %d, %s)' \
                           % (
                               remaining_occ,
                               bls_funcs.find_occ_level(remaining_occ),
                               unit_code,
                               req_aggregated_count,
                               'true')
                elif(table_name == 'BLS_OES_2016'):
                    sql += '(\'%s\', \'%s\', \'%s\', %d, %s)' \
                           % (
                               unit_code,
                               remaining_occ,
                               bls_funcs.find_occ_level(remaining_occ),
                               req_aggregated_count,
                               'true')
                else:
                    print("unknown table name")

                sql += ','

        print("sql generated for unit_code %s" % (unit_code))

        cur.execute("INSERT INTO _metro_employment_tool._metro_employment_tool_tables.\"%s\""
                    " VALUES " % (table_name) + sql[:-1] )

    print("data aggregated for %s" % table_name)
    conn.commit()

    cur.close()

def get_indexes_for_addition_removal(m, l1, l2):
    idx_del = []
    m.sort()
    for e in l2:
        idx_del.append(m.index(e))

    m = list(np.delete(m, idx_del))
    for e in l1:
        m.append(e)

    idx_add = []
    m.sort()
    for e in l1:
        idx_add.append(m.index(e))
    #use it as follows
    #take m, sort m, first del at idx_del, then insert 0 at idx_add
    return (m, idx_del, idx_add)

def get_Matrix2_Matrix3_indexes_to__add_remove(matrix_dict):
    m1 = set(matrix_dict[1])
    m2 = set(matrix_dict[2])
    m3 = set(matrix_dict[3])

    # get the occupations that are there in m1 but not in m2
    m1_add_0 = m3.difference(m1)
    m2_add_0 = m3.difference(m2)
    m1_remove = m1.difference(m3)
    m2_remove = m2.difference(m3)

    #now get the indexes for addition and removal
    final = (
        get_indexes_for_addition_removal(list(m1), m1_add_0, m1_remove),
        get_indexes_for_addition_removal(list(m2), m2_add_0, m2_remove)
    )

    return final

def create_csv_from_dict(d, unit_name, csv_name):
    col = d["columns"]
    col.insert(0, unit_name)
    df = pd.DataFrame(columns=col)
    del d["columns"]
    for k, v in d.items():
        v.insert(0, k)
        tdf = pd.DataFrame([v], columns=col)
        df = pd.concat([df, tdf])

    df.to_csv('./suitability_tables/%s.csv' % csv_name, index=False)
    print("csv written for %s" % csv_name)

def create_csv_for_suitability():
    occ_levels = ["Broad", "Detailed"]
    configurations = [('BLS_NEM_2016', 'ZCTA_OCC_COUNTS', 'BLS_OES_2016')]
    unit_code_map = {
        'BLS_NEM_2016' : 'IND_CODE',
        'BLS_OES_2016' : 'MSA_CODE',
        'ZCTA_OCC_COUNTS' : 'ZCTA_ID'
    }


    # ind_levels = [""] #todo make industry level aggregations
    cur = util.get_connection().cursor()
    for level in occ_levels:
        #using notations same as getSuitability.m provided by Dr. Shade
        matrix_list_occ = {
            1 : None,
            2 : None,
            3 : None
        }

        add_remove_matrices = {
            1 : {
                "add" : None,
                "remove" : None,
                "new_codes" : None
            },
            2 : {
                "add" : None,
                "remove" : None,
                "new_codes": None
            },
            3 : {
                "new_codes": None
            }
        }


        for index1, config in enumerate(configurations):
            matrix_to_table_map = {}
            for idx, table_name in enumerate(config):
                cur.execute('SELECT DISTINCT \"OCC_CODE\" '
                            'FROM _metro_employment_tool._metro_employment_tool_tables.\"%s\" '
                            'WHERE \"OCC_GROUP\" = \'%s\' '
                            'ORDER BY \"OCC_CODE\"'
                            % (table_name, level))
                matrix_list_occ[idx+1] = [occ_code[0] for occ_code in cur.fetchall()]
                matrix_to_table_map[idx+1] = table_name

            t1 = get_Matrix2_Matrix3_indexes_to__add_remove(matrix_list_occ)

            #fill in add_remove_matrices
            add_remove_matrices[1]["new_codes"] = t1[0][0]
            add_remove_matrices[1]["remove"] = t1[0][1]
            add_remove_matrices[1]["add"] = t1[0][2]
            add_remove_matrices[2]["new_codes"] = t1[1][0]
            add_remove_matrices[2]["remove"] = t1[1][1]
            add_remove_matrices[2]["add"] = t1[1][2]
            add_remove_matrices[3]["new_codes"] = copy.deepcopy(t1[0][0])  # todo this is ugly do better
            # len_inital = [0, 0, 0]
            # len_final = [0, 0, 0]
            #start making csv structures over here, temporarily putting them in a variable for debugging purposes
            #first we create table for m3, dict -> pandas dataframe -> csv
            for m_no in [1,2,3]:
                print("Caculating Matrix %s for config %d for level %s" % (matrix_to_table_map[m_no], index1+1, level))
                m_dict = {}
                m_dict['columns'] = add_remove_matrices[m_no]["new_codes"]

                #now create columns for each unit_code
                #first fetch all the unit_code
                cur.execute('SELECT DISTINCT \"%s\"'
                            'FROM _metro_employment_tool._metro_employment_tool_tables.\"%s\" '
                            'WHERE \"OCC_GROUP\" = \'%s\' '
                            'ORDER BY \"%s\"'
                            % (unit_code_map[matrix_to_table_map[m_no]], matrix_to_table_map[m_no], level, unit_code_map[matrix_to_table_map[m_no]]))

                unit_codes = [unit_code[0] for unit_code in cur.fetchall()]
                for unit_code in unit_codes:
                    # print("Working for %s %s" % (unit_code_map[matrix_to_table_map[m_no]], unit_code))
                    cur.execute('SELECT \"TOT_EMP\", \"OCC_CODE\" '
                                'FROM _metro_employment_tool._metro_employment_tool_tables.\"%s\" '
                                'WHERE \"OCC_GROUP\" = \'%s\' '
                                'AND \"%s\" = \'%s\' '
                                'ORDER BY \"OCC_CODE\"'
                                % (matrix_to_table_map[m_no], level, unit_code_map[matrix_to_table_map[m_no]], unit_code))
                    unit_code_occ_counts = [occ_count[0] for occ_count in cur.fetchall()]
                    # len_inital[m_no-1] = len(unit_code_occ_counts)
                    if m_no != 3:
                        unit_code_occ_counts = list(np.delete(unit_code_occ_counts, add_remove_matrices[m_no]["remove"]))
                        unit_code_occ_counts = list(np.insert(unit_code_occ_counts, add_remove_matrices[m_no]["add"], np.zeros(add_remove_matrices[m_no]["add"])))
                    m_dict[unit_code] = unit_code_occ_counts
                    # len_final[m_no-1] = len(unit_code_occ_counts)
                csv_name = '%s_config%d_level_%s.csv' % (matrix_to_table_map[m_no], index1+1, level)
                #now create the table from m_dict
                create_csv_from_dict(m_dict, unit_code_map[matrix_to_table_map[m_no]], csv_name)
            # print("Intial lengths : " + str(len_inital))
            # print("Final lengths : " + str(len_final))

if __name__ == '__main__':
    bls_funcs.get_latest_bls_nem()
    edp.store_occ_distributions_MSA()
    edp.store_occ_distribution_ZCTA()
    edp.clean_up_db_occ()
    aggregate_occ('BLS_NEM_2016', 0)
    aggregate_occ('BLS_OES_2016', 0)
    aggregate_occ('ZCTA_OCC_COUNTS', 0)
    # edp.store_occ_distribution_ZCTA()
    # aggregate_occ_bls_nem('ZCTA_OCC_COUNTS', 0)
    # aggregate_occ('BLS_OES_2016', 0)
    # create_csv_for_suitability()