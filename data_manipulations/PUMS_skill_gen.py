from data_manipulations import util
import logging
import json
from datetime import datetime

class PUMS_skill_generator:
    #important data structures that would be used later, also keep a way to store them in processing_data and retrieve them
    all_list = {
        "SOCP" : None,
        "SCHL" : None,
        "FOD1P" : None,
        "FOD2P" : None
    }

    # this will contain all the counts of each SCHL, FOD1P, FOD2P for each SOCP
    all_occ_info = {}
    all_occ_education_skills = {}
    all_education_skill = []

    def __init__(self):
        pass

    def create_all_lists(self):
        conn = util.get_connection()
        cur = conn.cursor()

        for field in PUMS_skill_generator.all_list:
            cur.execute("SELECT DISTINCT %s from _metro_employment_tool_tables.pums_education" % (field))
            self.all_list[field] = [val[0] for val in cur.fetchall() if val[0].strip() != 'nan']
            print("data retrieved for field %s" % (field))

        cur.close()

    def store_all_lists(self):
        f = open('./processing_data/PUMS_skill_generator_all_list.json', 'w')
        json.dump(self.all_list, f, indent=4, separators=(',',':'))

    def get_all_lists(self):
        self.all_list = json.load(open('./processing_data/PUMS_skill_generator_all_list.json'))
        print("all list loaded")
        logging.debug(self.all_list)

    def gen_all_occ_info_structure(self):
        self.all_occ_info = {}
        for socp in self.all_list["SOCP"]:
            t1 = {
                "SCHL" : {},
                "FOD1P" : {},
                "FOD2P" : {}
            }

            self.all_occ_info[socp] = t1
            for field in ["SCHL", "FOD1P", "FOD2P"]:
                for val in self.all_list[field]:
                    self.all_occ_info[socp][field][val] = 0
        print("all occ info ds created")

    def populate_all_occ_info(self):
        conn = util.get_connection()
        cur = None
        cur = conn.cursor()
        for occ_code, occ_info in self.all_occ_info.items():
            #now retrive all the tuples of that occ from db and update count of SCHL, FOD1P, FOD2P
            cur.execute("SELECT * FROM _metro_employment_tool_tables.pums_education WHERE socp = '%s'" % occ_code)
            print("populating for occ %s" % occ_code)
            total_counts = {"SCHL":0, "FOD1P":0, "FOD2P":0}
            for row in cur.fetchall():
                if row[1].strip() != 'nan':  #stripping because nan stored as 'nan   ' bcoz of char(6); todo treat this error, make db varchar(6)
                    occ_info["SCHL"][row[1]] += 1
                    total_counts["SCHL"] += 1
                if row[2].strip() != 'nan':
                    occ_info["FOD1P"][row[2]] += 1
                    total_counts["FOD1P"] += 1
                if row[3].strip() != 'nan':
                    occ_info["FOD2P"][row[3]] += 1
                    total_counts["FOD2P"] += 1
            occ_info["SCHL"]["total"] = total_counts["SCHL"]
            occ_info["FOD1P"]["total"] = total_counts["FOD1P"]
            occ_info["FOD2P"]["total"] = total_counts["FOD2P"]
            logging.debug('occ info generated for occ %s' % occ_code)
        cur.close()

    def store_all_occ_skill_values(self):
        conn = util.get_connection()
        sql = 'INSERT INTO _metro_employment_tool_tables.pums_education_skills VALUES '
        occ_count = 0
        for occ_code, occ_info in self.all_occ_info.items():
            # go through each dictionary object add up SCHL and <FOD1P, FOD2P>, then divide by respective totals and put in database
            SCHL_total = occ_info["SCHL"]["total"]
            FODP_total = occ_info["FOD1P"]["total"] + occ_info["FOD2P"]["total"]

            #popping off total keys for preventing inclusion into DB
            occ_info["SCHL"].pop('total')
            occ_info["FOD1P"].pop('total')
            occ_info["FOD2P"].pop('total')

            for k, v in occ_info['SCHL'].items():
                skill_value = v / SCHL_total
                sql += "('%s','%s','%s','%s'),\n" % (occ_code.strip(), k.strip(), 'SCHL', skill_value)

            for k, v in occ_info['FOD1P'].items():
                #adding value from FOD1P and FOD2P
                skill_count = v + occ_info['FOD2P'][k]
                skill_value = skill_count / FODP_total #basically out of all the degrees people have earned(whether first or second), it tells the proportion of that degree
                sql += "('%s','%s','%s','%s'),\n" % (occ_code.strip(), k.strip(), 'FODP', skill_value)
            occ_count += 1
            print("Progress: completed for occupation %s %s/%s" % (occ_code, occ_count, len(self.all_list['SOCP'])))

        logging.debug(sql[:3000])
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE _metro_employment_tool_tables.pums_education')
        cur.execute(sql[:-2])
        ans = input('commit to db:')
        if ans == 'Y':
            conn.commit()

    def gen_all_occ_info_final_structure(self):
        self.all_occ_education_skills = {}
        for socp in self.all_list["SOCP"]:
            self.all_occ_education_skills[socp] = {}
            for field in ["SCHL", "FOD1P"]:
                for val in self.all_list[field]:
                    self.all_education_skill.append(val)
                    self.all_occ_education_skills[field][val] = 0

    def fill_all_occ_education_skills(self):
        #gets all the occupation skill values from the database and fills up the final_skill_value_ds
        self.gen_all_occ_info_final_structure()
        conn = util.get_connection()
        cur = conn.cursor()
        for k, v in self.all_occ_education_skills:
            cur.execute("SELECT socp, education_skill_id, value "
                        "FROM _metro_employment_tool_tables.pums_education_skills "
                        "where socp = '%s'" % k)
            for row in cur.fetchall():
                v[row[1]] = row[3]

    def msa_education_skill_count(self):
        self.gen_all_occ_info_structure()
        self.fill_all_occ_education_skills()
        skill_values = self.all_occ_education_skills
        skill_list = self.all_education_skill

        conn = util.get_connection()
        cur = conn.cursor()

        # fetch all the avaiable MSAs
        cur.execute('SELECT DISTINCT ("MSA_CODE") from '
                    '_metro_employment_tool._metro_employment_tool_tables."BLS_OES_2016"')
        MSA_list = [msa[0] for msa in cur.fetchall()]

        sql = ''
        for msa in MSA_list:
            cur.execute('SELECT "MSA_CODE", "OCC_CODE", "TOT_EMP" from '
                        '_metro_employment_tool._metro_employment_tool_tables."BLS_OES_2016" '
                        'where '
                        '("OCC_GROUP" =\'detailed\' or "OCC_GROUP" = \'Broad\') and "MSA_CODE" = \'%s\' and "TOT_EMP" != -1' % (
                        msa))
            for skill in skill_list:
                tot_occ = 0
                tot_skill_val = 0
                for msa_row in cur.fetchall():
                    occ_code = msa_row[1]
                    emp_count = msa_row[3]
                    if (occ_code in skill_values):
                        tot_occ += emp_count
                        tot_skill_val += emp_count * skill_values[occ_code][skill]
                final_skill_val = tot_skill_val / tot_occ

    def test_all_ds(self):
        self.create_all_lists()
        self.store_all_lists()
        self.get_all_lists()
        self.gen_all_occ_info_structure()
        self.populate_all_occ_info()
        # self.store_all_occ_skill_values()
        # self.msa_education_skill_count()
        # self.create_csv_for_pums_education_skill()
        pass

    def create_csv_for_pums_education_skill(self):
        conn = util.get_connection()
        cur = conn.cursor()
        types = ["FODP", "SCHL"]
        #first fetch all different SOCP, then iterate through them and create the necessary columns
        cur.execute('SELECT distinct(socp) '
                     'FROM '
                     '_metro_employment_tool_tables.pums_education_skills')

        socp_l = [socp[0] for socp in cur.fetchall()]
        for type in types:
            f = open('.//pums_education_skill_csvs//%s.csv' % type, 'w')
            final_str = ""
            cur.execute('SELECT DISTINCT education_skill_id '
                        'FROM _metro_employment_tool_tables.pums_education_skills '
                        'WHERE skill_type = \'%s\' '
                        'ORDER BY education_skill_id;' % type)

            final_str += "Occupation Code,"
            for skill_id in cur.fetchall():
                final_str += ('%s,' % skill_id)
            final_str = final_str[:-1] + '\n'

            for socp in socp_l:
                final_str += ('%s,' % socp)


                cur.execute('SELECT *'
                            ' FROM _metro_employment_tool_tables.pums_education_skills'
                            ' WHERE skill_type = \'%s\' AND socp = \'%s\' '
                            ' ORDER BY education_skill_id;' % (type, socp))

                for t1 in cur.fetchall():
                    final_str += ('%s,' % t1[3])
                final_str = final_str[:-1] + '\n'

            f.write(final_str)
            f.close()

if __name__ == '__main__':
    # logging.basicConfig(filename='./logs/PUMS_skill_generator', level=logging.INFO, format='%(levelname)s:%(message)s')
    # logging.info('program started: %s' % (datetime.now().strftime('%m-%d %H:%M:%S')))
    skill_gen = PUMS_skill_generator()
    # skill_gen.test_all_ds()
    skill_gen.create_csv_for_pums_education_skill()
