import pandas as pd
from data_manipulations import util
import logging
from time import strftime, gmtime

def truncate_table_PUMS():
    conn = util.get_connection()
    cur = conn.cursor()
    cur.execute('TRUNCATE TABLE _metro_employment_tool_tables.pums_education')

def insert_into_db_from_sql(sql):
    conn = util.get_connection()
    cur = conn.cursor()
    cur.execute(sql[:-1])
    cur.close()
    conn.commit()

def read_PUMS_to_sql(chunksize=1000, sql_chunks_no=100, total_rows=int(15*1e6)):
    #idea is to first read say sql_chunk_no chunk from data, that gives us sql_chunk_no*chunksize rows
    truncate_table_PUMS()
    pum_files = ['ss16pusa.csv', 'ss16pusb.csv', 'ss16pusc.csv', 'ss16pusd.csv']
    approx_total_chunks = round(total_rows / chunksize)
    logging.info("approx_total_chunks:  %d" % approx_total_chunks)
    for pum in pum_files:
        chunks = pd.read_csv('./raw_data/%s' % pum, chunksize=chunksize)
        sql = 'INSERT INTO _metro_employment_tool_tables.pums_education VALUES '
        chunk_count = 0
        display_chunk_count = 0
        for chunk in chunks:
            for idx, row in chunk.iterrows():
                if(not row.isnull()['SOCP']):
                    if(not (row.isnull()['SCHL'] and row.isnull()['FOD1P'] and row.isnull['FOD2P'])):
                        socp_value = row['SOCP']
                        socp_value_compatible = socp_value[:2] + '-' + socp_value[2:]
                        sql += '(\'%s\',\'%s\',\'%s\',\'%s\'),' % (socp_value_compatible, row['SCHL'], row['FOD1P'], row['FOD2P'])
            chunk_count += 1
            display_chunk_count += 1

            if(chunk_count == sql_chunks_no):
                insert_into_db_from_sql(sql)
                sql = 'INSERT INTO _metro_employment_tool_tables.pums_education VALUES '
                chunk_count = 0
            if(display_chunk_count % 100 == 0):
                logging.info("For File  %s, chunks_completed %d / %d" % (pum, display_chunk_count, approx_total_chunks))
                print("number of chunks inserted: %d" % display_chunk_count)
        #handling last few chunks that might be left if total rows not multiple of sql_chunk_no*chunksize
        if chunk_count != 0:
            insert_into_db_from_sql(sql)
        logging.info("Data inserted successfully for file : %s" % pum)

if __name__ == '__main__':
    logging.basicConfig(filename='./logs/import_pums_logs', level=logging.INFO, format='%(levelname)s:%(message)s')
    logging.info('program started new: %s' % (strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    read_PUMS_to_sql()