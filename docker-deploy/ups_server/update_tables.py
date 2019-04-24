import psycopg2
import time
#need to insert user
#need to check the real status that we get from world
def init_world(world_id,curr):
    print("init table world")
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "INSERT INTO \"myUPS_world\" VALUES (%s,%s);"
    db_cur.execute(sql,(world_id,curr))
    db_conn.commit()
    db_conn.close()
    print("finished world")

def check_world(world_id):
    print("check world")
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "SELECT world_id FROM \"myUPS_world\" WHERE world_id = %s;"
    db_cur.execute(sql,(world_id,))
    results = db_cur.fetchall()
    print(results)
    db_conn.commit()
    db_conn.close()
    if results == []:
        return False
    print("finished check world")
    return True

def find_truck_id():
    print("find truck")
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "SELECT MAX(truck_id) FROM \"myUPS_truck\";"
    db_cur.execute(sql)
    results = db_cur.fetchall()
    truck_id = results[0][0]
    print(truck_id)
    db_conn.commit()
    db_conn.close()
    return truck_id

def check_account(world_id, account):
    print("find account")
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "SELECT user_id FROM \"myUPS_account\" WHERE user_id = %s;"
    db_cur.execute(sql, (account,))
    results = db_cur.fetchall()
    if results == []:
        return False
    else:
        return True

def change_world(world_id):
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "UPDATE \"myUPS_world\" SET curr = False WHERE world_id <> %s;"
    sql1 = "UPDATE \"myUPS_world\" SET curr = True WHERE world_id = %s;"
    db_cur.execute(sql, (world_id,))
    db_cur.execute(sql1, (world_id,))
    db_conn.commit()
    db_conn.close()
    
def init_trucks(pos_x, pos_y, num, world_id):
    print("init table trucks")
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "INSERT INTO \"myUPS_truck\" (cur_status,pos_x,pos_y,world_id) values (%s,'%s','%s',%s);"
    print(sql)
    db_cur.execute("delete from \"myUPS_truck\";")
    db_cur.execute("ALTER SEQUENCE \"myUPS_truck_truck_id_seq\" RESTART WITH 1;")
    for i in range(0, num):
        db_cur.execute(sql,("i",pos_x,pos_y,world_id))
    db_conn.commit()
    db_conn.close()
    print("finished")

#when need to update truck status, query world and get the info of truck
def update_truck(truck_id, status, pos_x, pos_y, world_id):
    print("update truck status")
    print("%s   %s   %s   %s   %s" % (truck_id, status, pos_x, pos_y, world_id))
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    if pos_x == None:
        sql = "UPDATE \"myUPS_truck\" SET cur_status = %s WHERE truck_id = '%s' AND world_id = %s; "
        db_cur.execute(sql,(status,truck_id,world_id))
    else:
        sql = "UPDATE \"myUPS_truck\" SET cur_status = %s, pos_x = '%s', pos_y = '%s' WHERE truck_id = '%s' AND world_id = %s; "
        db_cur.execute(sql,(status,pos_x,pos_y,truck_id,world_id))
    db_conn.commit()
    db_conn.close()
    print(status)
    print("finish update truck")

def update_dest(package_id, pos_x, pos_y, world_id):
    print("update package destination")
    print("%s   %s   %s " % (package_id, pos_x, pos_y))
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "UPDATE \"myUPS_package\" SET dest_x = '%s', dest_y = '%s' WHERE package_id = '%s' AND world_id = %s; "
    db_cur.execute(sql,(pos_x,pos_y,package_id,world_id))
    db_conn.commit()
    db_conn.close()
    print("finish update dest")

# def tr_pkg(package_id,truck_id,world_id):
#     print("tr pkg")
#     db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
#     db_cur = db_conn.cursor()
#     sql = "UPDATE \"myUPS_package\" SET truck_id = %s where package_id = %s and world_id = %s;"
#     db_cur.execute(sql,(truck_id,package_id,world_id))
#     db_conn.commit()
#     db_conn.close()
#     print("finished tr pkg")

#need to delete the table when initialize world
def ins_pkg(package_id, account, truck_id, wh_id, wh_addr_x, wh_addr_y, dest_x, dest_y,world_id):
    print("ins pkg")
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "INSERT INTO \"myUPS_package\" (ready_for_pickup_time, package_id, user_id, truck_id, wh_id, wh_addr_x, wh_addr_y, dest_x, dest_y, cur_status, world_id) values (%s,'%s',%s,%s,'%s','%s','%s','%s','%s',%s,%s);"
    current = time.time()
    now = time.ctime(current)
    db_cur.execute(sql,(now, package_id, account, truck_id, wh_id, wh_addr_x, wh_addr_y, dest_x, dest_y, "p", world_id))
    # print(sql)
    db_conn.commit()
    db_conn.close()
    print("finished")

#when package is loaded, record the time and change the boolean field
def delivering_pkg(package_id,world_id):
    print("up pkg")
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "UPDATE \"myUPS_package\" SET cur_status = %s, load_time = %s where package_id  = '%s' and world_id = %s;"
    current = time.time()
    now = time.ctime(current)
    db_cur.execute(sql,("o",now,package_id,world_id))
    db_conn.commit()
    db_conn.close()
    print("finished uppkg")

#when pkg is delivered, record the time
def delivered_pkg(package_id,world_id):
    print("delivered pkg")
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "UPDATE \"myUPS_package\" SET cur_status = %s, delivered_time = %s where package_id  = '%s' and world_id = %s;"
    current = time.time()
    now = time.ctime(current)
    db_cur.execute(sql,("d",now,package_id,world_id))
    db_conn.commit()
    db_conn.close()
    print("finished delivered")

#return truck_id for a package
def req_truck_package(package_id):
    print("find truck_id")
    pack_id = int(package_id)
    print(type(package_id))
    print(pack_id)
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "SELECT truck_id, dest_x, dest_y FROM \"myUPS_package\" WHERE package_id = '%s';"
    db_cur.execute(sql, (package_id,))
    results = db_cur.fetchall()
    truck_id = results[0][0]
    dest_x = results[0][1]
    dest_y = results[0][2]
    print(truck_id)
    print(dest_x)
    print(dest_y)
    db_conn.commit()
    db_conn.close()
    print("finished find truck_id and destination")
    return truck_id, dest_x, dest_y

# req_truck_package(20)

def req_email(pack_id, world_id):
    print("find email")
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "SELECT email FROM auth_user WHERE id = (SELECT user_id FROM \"myUPS_account\" WHERE id = (SELECT user_id From \"myUPS_package\" WHERE package_id = '%s'));"
    db_cur.execute(sql,(pack_id,))
    results = db_cur.fetchall()
    if results == []:
        print("no email found")
        return None
    email = results[0][0]
    print(email)
    db_conn.commit()
    db_conn.close()
    print("finished find email")
    return email

    # select user_id from "myUPS_account" where id = 

def req_package_to_pack(truck_id, wh_x, wh_y, world_id):
    print("find package_id to pack")
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "SELECT package_id FROM \"myUPS_package\" WHERE truck_id = %s AND wh_addr_x = '%s' AND wh_addr_y = '%s' AND cur_status = \'p\' AND world_id = %s;"
    db_cur.execute(sql,(truck_id, wh_x, wh_y, world_id))
    results = db_cur.fetchall()
    pack_id = results[0][0]
    db_conn.commit()
    db_conn.close()
    print("finished find package_id to pack")
    return pack_id

# req_package_to_pack(1, 2, 3, 1)

#if don't have this roll, what will return 
def req_truck(world_id):
    print("ask a truck to go pickup")
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql_i = "SELECT TRUCK_ID FROM \"myUPS_truck\" WHERE cur_status = \'i\' and world_id = %s limit 1;"
    print(sql_i)
    db_cur.execute(sql_i,(world_id,))
    results = db_cur.fetchall()
    # if results == []:
    #     sql_t = "SELECT TRUCK_ID FROM \"myUPS_truck\" WHERE cur_status = \'t\' and world_id = %s limit 1;"
    #     db_cur.execute(sql_t,(str(world_id)))
    #     results = db_cur.fetchall()
    #     if results == []:
    #         sql_a = "SELECT TRUCK_ID FROM \"myUPS_truck\" WHERE cur_status = \'a\' and world_id = %s limit 1;"
    #         db_cur.execute(sql_a,(str(world_id)))
    #         results = db_cur.fetchall()
    if results == []:
        return None
    #if there is no truck available, need to wait until find a truck
    truck_id = results[0][0]
    db_conn.commit()
    db_conn.close()
    print("finished req truck")
    return truck_id

def req_pkg_status(package_id,world_id):
    print ("ask current status of a package")
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "SELECT cur_status,truck_id FROM \"myUPS_package\" WHERE package_id = '%s' and world_id = %s;"
    db_cur.execute(sql,(package_id,world_id))
    results = db_cur.fetchall()
    if results == []:
        return None,None
    status = results[0][0]
    truck_id = results[0][1]
    db_conn.commit()
    db_conn.close()
    print("finished req status")
    return status,truck_id

def req_ready_for_pickup_time(package_id,world_id):
    print("ready_for_pickup_time")
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "SELECT ready_for_pickup_time FROM \"myUPS_package\" WHERE package_id = '%s' and world_id = %s;"
    db_cur.execute(sql,(package_id,world_id))
    results = db_cur.fetchall()
    ready_for_pickup_time = results[0][0]
    return ready_for_pickup_time

def req_load_time(package_id,world_id):
    print("load_time")
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "SELECT load_time FROM \"myUPS_package\" WHERE package_id = '%s' and world_id = %s;"
    db_cur.execute(sql,(package_id,world_id))
    results = db_cur.fetchall()
    load_time = results[0][0]
    return load_time

def req_delivered_time(package_id,world_id):
    print("delivered_time")
    db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
    db_cur = db_conn.cursor()
    sql = "SELECT delivered_time FROM \"myUPS_package\" WHERE package_id = '%s' and world_id = %s;"
    db_cur.execute(sql,(package_id,world_id))
    results = db_cur.fetchall()
    delivered_time = results[0][0]
    return delivered_time

# def update_truck_status(status,truck_id,world_id):
#     print("update truck status")
#     db_conn = psycopg2.connect(host="db",database="postgres", user="postgres", port="5432")
#     db_cur = db_conn.cursor()
#     sql = "UPDATE \"myUPS_truck\" SET cur_status = %s where truck_id  = %s and world_id = %s;"
#     now = time.time()
#     db_cur.execute(sql,(status,str(package_id),str(world_id)))
#     db_conn.commit()
#     db_conn.close()
#     print("finished update truck status")








# pos_x = "1"
# pos_y = "2"
# init_world(5,True)
# init_trucks(pos_x,pos_y,3,"1")
# ins_pkg(6,1,2,1,1,1,1,1)
# pkg_num = "6"
# truck_id = "1"
# load_pkg(pkg_num,"1")
# tr_pkg(pkg_num,truck_id,"1")
# update_truck(1,"b","2","3","1")
# update_truck(2,"b","2","3","1")
# update_truck(3,"b","2","3","1")
# delivered_pkg(pkg_num,"1")
# truck_id = req_truck("1")
# print(truck_id)
# status = req_status(pkg_num,"1")
# print(status)
# ready_for_pickup_time = ""
# ready_for_pickup_time = req_load_time(pkg_num,"1")
# print(ready_for_pickup_time,"1")
# print(req_load_time(pkg_num,"1"))
# print(req_delivered_time(pkg_num,"1"))
# print(check_world("1"))

# find_truck_id()

# change_world("3")
# init_world(1,False)
# init_trucks(1,1,1,1)
# ins_pkg(1, None, 1, 1, 1, 1, 1, 1,1)
# p,des_x,desy = req_truck_package(1)
# print(p)
# print(des_x)
# print(desy)
# print(req_truck(1))

#test update truck
# update_truck(1, "i", None, None, 1)

# init_world(1, True)
# init_trucks(1, 1, 1, 1)
# for i in range(2, 10):
#     ins_pkg(i, 1, 1, 1, 2, 3, 123, 123, 1)

# ins_pkg(4, 3, 1, 1, 2, 3, 123, 123, 1)
# delivering_pkg(4, 1)
# req_email(1, 1)