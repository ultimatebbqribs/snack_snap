import psycopg2
import os
DB_URL = os.environ.get('DATABASE_URL', 'dbname=snack_snap')

def sql_select(db_query, params=[]):
    conn = psycopg2.connect('dbname=DB_URL')
    cur = conn.cursor()
    cur.execute(db_query,params)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def sql_write(db_query, params=[]):
    conn = psycopg2.connect('dbname=DB-URL')
    cur = conn.cursor()
    cur.execute(db_query,params)
    conn.commit()
    cur.close()
    conn.close()
    return