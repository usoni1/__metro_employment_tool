from bs4 import BeautifulSoup
from data_manipulations import util
import requests
import urllib.request
import pandas
import re
import psycopg2


def find_ind_level(code):
    if(code == '900000'):
        return "Special"

    if(code.isdigit()):
        no_digits = len(code.replace('0', ''))
        if(no_digits == 2):
            return "Sector"
        elif(no_digits == 3):
            return  "Subsector"
        elif(no_digits == 4):
            return "Ind Group"
        elif(no_digits == 5):
            return "NAICS Group"
        elif(no_digits == 6):
            return "National Industry"
        else:
            return "UnexpectedCode"
    else:
        return "Special"

def find_occ_level(code):
    if(code == '00-0000'):
        return "Special"
    if(code == '15-1200'):
        return "Minor"
    if(code == '51-5100'):
        return "Minor"
    if(code == '31-1100'):
        return "Minor"
    if(code == '15-1100'):
        return "Minor"
    no_digits = len(re.sub(r"0*$|-", '', code))
    if(no_digits == 2):
        return "Major"
    elif(no_digits == 3):
        return "Minor"
    elif(no_digits == 5):
        return "Broad"
    elif(no_digits == 6):
        return "Detailed"
    else:
        return "UnexpectedCode"

def get_latest_bls_nem():
    conn = util.get_connection()
    cur = conn.cursor()
    #for BLS_NEM 2016-2026 tables, going through the main website, downloading the xlsx, and then putting it all in the database
    req = requests.get('https://www.bls.gov/emp/ep_table_109.htm')
    soup = BeautifulSoup(req.content, "html5lib")
    main_content = soup.find('td', id='main-content-td')
    table_rows = main_content.find_all('tr')
    base_link='https://www.bls.gov'
    sql = ''
    for rows in table_rows[1:-1]:
        p_tags = [p_tag.text for p_tag in rows.find_all('p')]
        industry_title = p_tags[0]
        industry_code = p_tags[1]
        industry_type = p_tags[2]
        industry_level = find_ind_level(industry_code)
        xls_link_tag = rows.find_all('p')[-1]
        final_xls_link = base_link + xls_link_tag.a['href']
        urllib.request.urlretrieve(final_xls_link, './bls_nem_temp_xlsx/%s.xlsx' % (industry_code))
        reader = pandas.read_excel('./bls_nem_temp_xlsx/%s.xlsx' % (industry_code))
        # print(industry_code, industry_title, industry_type, industry_level)
        for index, row in reader.iterrows():
            if(not row.isnull()[2] and row[2] != 'Title'):
                occ_code = row[1]
                occ_title = row[2]
                occ_count = row[3]*1000
                occ_level = find_occ_level(occ_code)
                sql += '(\'%s\',\'%s\',\'%s\',\'%s\',%d, %s)' % (industry_code, industry_level, occ_code, occ_level, occ_count, 'false')
                sql += ','
                # print(occ_code, occ_title, occ_count, occ_level)
        print("Data entered for industry %s" % (industry_code))


    # print("SQL statement created \n first few bits of SQL: ")
    # print(sql[:1000])


    cur.execute("TRUNCATE _metro_employment_tool."
                "_metro_employment_tool_tables.\"BLS_NEM_2016\"")

    cur.execute("INSERT INTO _metro_employment_tool._metro_employment_tool_tables.\"BLS_NEM_2016\""
                " VALUES " + sql[:-1])

    commit_go_ahead = input("Go ahead with commit...Y/N...\n")
    if(commit_go_ahead == 'Y'):
        conn.commit()
    cur.close()

if __name__ ==  '__main__':
    # conn = util.get_connection()
    # cur = conn.cursor()
    # cur.execute("INSERT INTO _metro_employment_tool._metro_employment_tool_tables.\"BLS_NEM_2016\""
    #                    "VALUES " + "('110000', 'major', '11-1100', 'major', 5000, 'false')")
    get_latest_bls_nem()