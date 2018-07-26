import psycopg2

def get_connection():
    hostname = 'localhost'
    username = 'metro_insight_admin'
    password = 'password'
    database = '_metro_employment_tool'
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=5433)
    return conn

if __name__ == '__main__':
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('select count(*) from _metro_employment_tool_tables."BLS_NEM_2016"')
    print(cur.fetchall())