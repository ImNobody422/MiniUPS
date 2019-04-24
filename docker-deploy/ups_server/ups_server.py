import os
import psycopg2
import socket
import threading

import ups_world_pb2
import ups_amazon_pb2

from ups_build_msg import build_world
from ups_send_recv import *

from update_tables import *
from ups_handler import amazon_recver, world_recver
from delete import deleteall

world_host = "vcm-9394.vm.duke.edu"
world_port = 12345
amazon_port = 8888

database_host = "db"
database_port = 5432

deleteall()

world_id = "1"
# connect to the database
# while 1:
#     try:
#         db = psycopg2.connect(dbname = "finalpj", user = "postgres", password = "111111", host = "127.0.0.1", port = "5432")
#         dbcursor = db.cursor()
#     except psycopg2.OperationalError:
#         continue
#     else:
#         print("connection to databse succeed")
#         break

# ----------------------------------------------------------------------------------
# Step 1 : connect to the world
# ----------------------------------------------------------------------------------
world_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
world_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
while 1:
    try:
        world_socket.connect((world_host, world_port))
    except BaseException as e:
        print(e)
        continue
    else:
        break
# print("success connected to world")

# ----------------------------------------------------------------------------------
# Step 2 : Initialize the World
# ----------------------------------------------------------------------------------
# custom the number of trucks and their position
truck_num = 50
pos_x = 0
pos_y = 0
# if world exist:
world_exist = check_world(world_id)
UConnect = ups_world_pb2.UConnect()
while 1:
    try:
        if world_exist:
            build_world(UConnect,  world_id, 0, pos_x, pos_y, 0)
            print("successfully massed up")
        else:
            print("successfully fucked up")
            truck = find_truck_id()
            max_id = 1
            if truck != None:
                max_id = truck + 1
            build_world(UConnect, None, truck_num, pos_x, pos_y, max_id)
        send_msg(UConnect, world_socket)
        # print(UConnect.worldid)
        # print(UConnect.isAmazon)
        UConnected = recv_connected(world_socket)
        print(UConnected.worldid)
        print(UConnected.result)
        if UConnected.result != "connected!":
            continue
        world_id = str(UConnected.worldid)
        break
    except (ConnectionRefusedError, ConnectionResetError, ConnectionError, ConnectionAbortedError) as e:
        print(e)
        continue
if not world_exist:
    init_world(world_id, True)
    init_trucks(pos_x, pos_y, truck_num, world_id)
change_world(world_id)
UCommandspeed = ups_world_pb2.UCommands()
UCommandspeed.simspeed = 30000
send_msg(UCommandspeed, world_socket)

# Uconnect = ups_world_pb2.UConnect()
# build_world(Uconnect, world_id, truck_num, pos_x, pos_y, 1)
# # initialize the trucks in database
# # send_msg(UConnect, world_socket)
# # UConnected = recv_connected(world_socket)
# # print(UConnected.worldid)
# # print(UConnected.result)
# # change_world(world_id)

# ----------------------------------------------------------------------------------
# Step 3 : Connect to Amazon
# ----------------------------------------------------------------------------------
amazon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
amazon.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Socket successfully created")
amazon.bind(('', amazon_port))
print("socket binded to %s" %(amazon_port))

amazon.listen(5)
print("socket is listening")

amazon_socket, addr = amazon.accept()
print('Got connection from', addr)

UACommands = ups_amazon_pb2.UACommands()
UACommands.world_id = int(world_id)
print(UACommands)
send_msg(UACommands, amazon_socket)

# ----------------------------------------------------------------------------------
# Step 4 : Start to handle Requests
# ----------------------------------------------------------------------------------
# try:
thread1 = threading.Thread(target=amazon_recver, name="amazon", args=(world_id, amazon_socket, world_socket,))
thread1.start()
thread2 = threading.Thread(target=world_recver, name="world", args=(world_id, world_socket, amazon_socket,))
thread2.start()
while 1:
    pass
# except KeyboardInterrupt as k:
#     print("ctrl c pressed")
#     # disconnect 功能
#     UACommand = ups_amazon_pb2.UACommands()
#     UACommand.disconnect = True
#     send_msg(UACommand, amazon_socket)
#     UDisconn = ups_world_pb2.UCommands()
#     UDisconn.disconnect = True
#     send_msg(UDisconn, world_socket)