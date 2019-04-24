from ups_send_recv import *
from update_tables import *
from ups_build_msg import *
import ups_world_pb2
import ups_amazon_pb2
import sys, os
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import smtplib

seqnum = 1
seq_mutex = threading.Lock()
# locks = []  # lock the packages when need to change their status

acks = [] # store ack message
ack_mutex = threading.Lock()
# lock for acks[]

def send_email(To, msg):
    host = "smtp.gmail.com"
    port = 587
    From = "DukeUpsOfficial@gmail.com"
    pwd = "UpsOfficial+1s"
    s = smtplib.SMTP(host, port)
    s.starttls()
    s.login(From, pwd)
    SUBJECT = "UPS Notification!"
    message = 'Subject: {}\n\n{}'.format(SUBJECT, msg)
    s.sendmail(From, To, message)
    s.quit()
    return


def get_curr_seqnum():
    # lock
    seq_mutex.acquire()
    global seqnum
    seq = seqnum
    seqnum += 1
    seq_mutex.release()
    return seq

def check_ack(seq):
    global acks
    if seq in acks:
        # lock maybe
        # acks.remove(seq)
        # release
        return True
    else:
        return False

def send_and_wait(msg, socket, seq):
    while 1:
        send_msg(msg, socket)
        time.sleep(10)
        if check_ack(seq):
            break
    return

def send_ack_world(world_socket, ack):
    UCommand = ups_world_pb2.UCommands()
    world_acks(UCommand, ack)
    send_msg(UCommand, world_socket)

# ----------------------------------------------------------------------------------
# Handle Amazon Message
# ----------------------------------------------------------------------------------

def Gopickup(get_truck, world_id, world_socket):
    # get package_id, ups_account, warehouse_id, wh_location, destination
    # 生成 new package into database, status "p"
    # 分配一辆 truck 给package, check truck status in database
    # send GoPickup message to world
    # after recv acks, change truck status to "traveling"
    seq = get_curr_seqnum()
    packid = get_truck.order_id
    account = None
    truck = 0
    while 1:
        truck = req_truck(world_id)
        if truck != None:
            break
    if get_truck.HasField("ups_account"):
        if check_account(world_id, get_truck.ups_account):
            account = get_truck.ups_account
        # check account exist or not
    whid = get_truck.warehouse_id
    wh_x = get_truck.location_x
    wh_y = get_truck.location_y
    dest_x = get_truck.destination_x
    dest_y = get_truck.destination_y
    ins_pkg(packid, account, truck, whid, wh_x, wh_y, dest_x, dest_y, world_id)
    UCommand = ups_world_pb2.UCommands()
    world_gopickup(UCommand, truck, whid, seq)
    update_truck(truck, "t", None, None, world_id)
    send_and_wait(UCommand, world_socket, seq)
    # Do we need to query truck status?
    # Update Truck Status to "t"
    return

def GoDeliver(init_delivery, world_id, world_socket):
    # get package_id
    # get truck_id, destination from database
    # send GoDeliver to World
    # after recv acks, change truck status to "d", change package status to "o" (out for deliver)
    # may need lock to secure the package status, if there is any change destination request
    # can add new mutex when creating a new package, release it when the package is delivered
    seq = get_curr_seqnum()
    packid = init_delivery.package_id
    truck, dest_x, dest_y = req_truck_package(packid)
    UCommand = ups_world_pb2.UCommands()
    world_godeliver(UCommand, truck, seq)
    deliver = UCommand.deliveries[0]
    world_delocation(deliver, packid, dest_x, dest_y)
    # update truck status to "delivering"
    update_truck(truck, "d", None, None, world_id)
    # update package status to 
    delivering_pkg(packid, world_id)
    To = req_email(packid, world_id)
    if To != None:
        msg = "Your package is on its way to meet you!"
        send_email(To, msg)
    send_and_wait(UCommand, world_socket, seq)    
    return

# We can still change the destination from frontend
def ChangeDest(change_destination, world_id, world_socket, amazon_socket):
    # this can only happens before the package is delivered
    # which means the package_status is before "d"
    # get package_id, new destination
    # change package information in database
    # resend GoDeliver message to World
    # Amazon should only send this message after the
    # when should Amazon send this message???????
    # a truck only takes one package, will deliver it right after package is loaded
    # This is why the package field is only "required" not "repeated"
    # should mention this in tomorrow's meeting
    # maybe we just should not change the destination from amazon side

    # reply a message indicating whether the destination change is success or not
    packid = change_destination.package_id
    dest_x = change_destination.new_destination_x
    dest_y = change_destination.new_destination_y
    stat, truck = req_pkg_status(packid, world_id)
    UACommand = ups_amazon_pb2.UACommands()
    if stat != "p":
        amazon_dest_change(UACommand, packid, dest_x, dest_y, False)
        send_msg(UACommand, amazon_socket)
    else:
        # seq = get_curr_seqnum()
        update_dest(packid, dest_x, dest_y, world_id)
        amazon_dest_change(UACommand, packid, dest_x, dest_y, True)
        send_msg(UACommand, amazon_socket)
        # UCommand = ups_world_pb2.UCommands()
        # world_godeliver(UCommand, truck, seq)
        # deliver = UCommand.deliveries[0]
        # world_delocation(deliver, packid, dest_x, dest_y)
        # send_and_wait(UCommand, world_socket, seq)
    return

def Disconnect_world(world_socket):
    seq = get_curr_seqnum()
    UCommand = ups_world_pb2.UCommands()
    UCommand.disconnect = True
    send_and_wait(UCommand, world_socket, seq)
    sys.exit()
    return


# ----------------------------------------------------------------------------------
# Handle World Message
# ----------------------------------------------------------------------------------

def Arrive_Finish(completions, world_id, amazon_socket, world_socket):
    # get truck_id, wh_location, truck status
    # change truck status to "l"
    # send truck_arrived to Amazon
    send_ack_world(world_socket, completions.seqnum)
    truck_id = completions.truckid
    wh_x = completions.x
    wh_y = completions.y
    update_truck(truck_id, "l", wh_x, wh_y, world_id)
    UACommand = ups_amazon_pb2.UACommands()
    # print("when arrive at warehouse")
    # print(UACommand)
    # find package id
    pack_id = req_package_to_pack(truck_id, wh_x, wh_y, world_id)
    amazon_truck_arrive(UACommand, wh_x, wh_y, truck_id, pack_id)
    send_msg(UACommand, amazon_socket)
    # print("after send")
    return

def Deliver_Finish(completions, world_id, world_socket):
    # get truck_id, package_id
    # change truck status to "i" (IDLE)
    # change truck current location
    send_ack_world(world_socket, completions.seqnum)
    truck_id = completions.truckid
    addr_x = completions.x
    addr_y = completions.y
    update_truck(truck_id, "i", addr_x, addr_y, world_id)
    return

def Completion_Handler(completions, world_id, amazon_socket, world_socket):
    if completions.status == "IDLE":
        Deliver_Finish(completions, world_id, world_socket)
    else:
        print("enter arrive handler")
        Arrive_Finish(completions, world_id, amazon_socket, world_socket)
    return

def Deliver_Handler(delivered, world_id, amazon_socket, world_socket):
    # get truck_id, package_id
    # change the package status to "d"
    # send delivered to Amazon
    send_ack_world(world_socket, delivered.seqnum)
    truck = delivered.truckid
    pack_id = delivered.packageid
    print(type(pack_id))
    print(pack_id)
    delivered_pkg(pack_id, world_id)
    UACommand = ups_amazon_pb2.UACommands()
    amazon_delivered(UACommand, pack_id)
    print(UACommand)
    send_msg(UACommand, amazon_socket)
    To = req_email(pack_id, world_id)
    if To != None:
        msg = "Your package has been successfully delivered!\nEnjoy your time!"
        send_email(To, msg)
    return

def Query_Handler(truckstatus):
    return

def Ack_Handler(acks_from_world):
    # add into a vector waiting for check
    # ack lock
    global acks
    for ack in acks_from_world:
        acks.append(ack)
    return

def Disconnect_amazon(finished):
    # send disconnect information to world
    # after recv finished
    # exit
    os._exit(0)
    return

def Error_Handler(error):
    # print what's wrong
    print(error)
    return

# ----------------------------------------------------------------------------------
# Two Main Functions
# ----------------------------------------------------------------------------------

def world_recver(world_id, world_socket, amazon_socket):
    num_threads = 5
    pool = ThreadPoolExecutor(num_threads)
    while 1:
        # set the number of threads as you want    
        UResponse = recv_world_msg(world_socket)
        print("recv from world")
        print(UResponse)
        print("recv finished")
        for a in range(0, len(UResponse.completions)):
            pool.submit(Completion_Handler, UResponse.completions[a], world_id, amazon_socket, world_socket)
        for b in range(0, len(UResponse.delivered)):
            pool.submit(Deliver_Handler, UResponse.delivered[b], world_id, amazon_socket, world_socket)
        for c in range(0, len(UResponse.truckstatus)):
            pool.submit(Query_Handler, UResponse.truckstatus[c], world_id)
        if len(UResponse.acks):
            pool.submit(Ack_Handler, UResponse.acks)
        for d in range(0, len(UResponse.error)):
            pool.submit(Error_Handler, UResponse.error[d], world_id)
        if UResponse.HasField("finished"):
            pool.submit(Disconnect_amazon, UResponse.finished, world_id)
    return

def amazon_recver(world_id, amazon_socket, world_socket):
    num_threads = 5
    pool = ThreadPoolExecutor(num_threads)
    while 1:
        AUCommands = recv_amazon_msg(amazon_socket)
        print("recv from amazon")
        print(AUCommands)
        print("recv finished")
        if AUCommands.HasField("get_truck"):
            pool.submit(Gopickup, AUCommands.get_truck, world_id, world_socket)
        if AUCommands.HasField("init_delivery"):
            pool.submit(GoDeliver, AUCommands.init_delivery, world_id, world_socket)
        if AUCommands.HasField("change_destination"):
            pool.submit(ChangeDest, AUCommands.change_destination, world_id, world_socket, amazon_socket)
        if AUCommands.HasField("disconnect"):
            pool.submit(Disconnect_world, world_socket)
    return

# U = ups_amazon_pb2.AUCommands()
# U.disconnect = False
# if not U.HasField("get_truck"):
#     print("right")
# print(U.HasField("get_truck"))