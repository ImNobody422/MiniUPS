import ups_world_pb2
import ups_amazon_pb2

# tested
def build_world(UConnect, world_id, truck_num, pos_x, pos_y, start_id):
    # UConnect = ups_world_pb2.UConnect()
    for i in range(0, truck_num):
        truck = UConnect.trucks.add()
        truck.id = start_id
        truck.x = pos_x
        truck.y = pos_y
        start_id += 1
    UConnect.isAmazon = False
    if world_id != None:
        UConnect.worldid = int(world_id)
    # return UConnect

# tested
def world_gopickup(UCommands, truck_id, whid, seqnum):
    pickup = UCommands.pickups.add()
    pickup.truckid = truck_id
    pickup.whid = whid
    pickup.seqnum = seqnum

# tested
def world_delocation(UGoDeliver, packid, x, y):
    pos = UGoDeliver.packages.add()
    pos.packageid = packid
    pos.x = int(x)
    pos.y = int(y)
    
# tested
def world_godeliver(UCommands, truck_id, seqnum):
    deliver = UCommands.deliveries.add()
    deliver.truckid = truck_id
    deliver.seqnum = seqnum

# tested
def world_query(UCommands, truck_id, seqnum):
    query = UCommands.queries.add()
    query.truckid = truck_id
    query.seqnum = seqnum

def world_acks(UCommands, ack):
    UCommands.acks.append(ack)

# Amazon Message
# tested
def amazon_truck_arrive(UACommands, wh_x, wh_y, truck_id, pack_id):
    UACommands.truck_arrived.wh_x = int(wh_x)
    UACommands.truck_arrived.wh_y = int(wh_y)
    UACommands.truck_arrived.truck_id = int(truck_id)
    UACommands.truck_arrived.package_id = int(pack_id)

# tested
def amazon_delivered(UACommands, pack_id):
    UACommands.package_delivered.package_id = pack_id

# tested
def amazon_dest_change(UACommands, pack_id, dest_x, dest_y, is_success):
    UACommands.destination_changed.new_destination_x = dest_x
    UACommands.destination_changed.new_destination_y = dest_y
    UACommands.destination_changed.package_id = pack_id
    UACommands.destination_changed.success = is_success

# tested
def amazon_disconnect(UACommands, disconn):
    UACommands.disconnect = disconn

def amazon_world_id(UACommands, world_id):
    UACommands.world_id = world_id

# -------------------------------TEST-------------------------------
# U = build_world(1, 5, 1,2, 6)
# for i in range(0, 5):
#     print(U.trucks[i].id)
# U = ups_world_pb2.UCommands()
# world_godeliver(U, 2, 1)
# de = U.deliveries.add()
# for i in range(0, 5):
#     world_delocation(de, i, 1, 4)
# for d in range(0, 5):
#     print("packid : %d, x: %d, y: %d" % (de.packages[d].packageid, de.packages[d].x, de.packages[d].y))
# for i in range(0, 5):
#     world_query(U, i, i)
# for d in range(0, 5):
#     print("truckid : %d, seq : %d" % (U.queries[d].truckid, U.queries[d].seqnum))
# U = ups_amazon_pb2.UACommands()
# amazon_truck_arrive(U, 1, 2)
# amazon_add_pack_to_truck(U.truck_arrived, 4)
# print(U.package_and_order_id.package_id)
# print(U.package_and_order_id.order_id)
# print(U.truck_arrived.warehouse_id)
# print(U.truck_arrived.truck_id)
# print(U.truck_arrived.package_id[0])
# amazon_dest_change(U, 4, True)
# print(U.destination_changed.package_id)
# print(U.destination_changed.success)
# amazon_disconnect(U, False)
# print(U.disconnect)
# U = ups_amazon_pb2.UACommands()
# amazon_world_id(U, 4)
# print(U.world_id)