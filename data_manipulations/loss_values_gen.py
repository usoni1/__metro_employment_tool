import psycopg2

def generate_occ_loss_values(conn):
    cur = conn.cursor()
    cur.execute('SELECT * ')
    pass

if __name__ == '__main__':
    hostname = 'localhost'
    username = 'metro_insight_admin'
    password = 'password'
    database = '_metro_employment_tool'

    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=5433)

    generate_occ_loss_values(conn)
    pass