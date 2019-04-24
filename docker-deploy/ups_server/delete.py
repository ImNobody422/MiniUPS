import psycopg2
#need to insert user
#need to check the real status that we get from world
def deleteall():
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "delete from \"myUPS_package\";delete from \"myUPS_truck\";delete from \"myUPS_account\";delete from \"myUPS_world\";"
    db_cur.execute(sql)
    db_cur.execute("delete from \"myUPS_truck\";")
    db_cur.execute("ALTER SEQUENCE \"myUPS_truck_truck_id_seq\" RESTART WITH 1;")
    db_cur.execute("ALTER SEQUENCE \"auth_user_id_seq\" RESTART WITH 1;")
    db_cur.execute("ALTER SEQUENCE \"myUPS_account_id_seq\" RESTART WITH 1;")
    db_cur.execute("delete from \"auth_user\";")
    db_conn.commit()
    db_conn.close()
    print("finished delete")

# deleteall()