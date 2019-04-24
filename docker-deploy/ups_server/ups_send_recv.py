from google.protobuf.internal.encoder import _VarintEncoder
from google.protobuf.internal.decoder import _DecodeVarint32

import ups_world_pb2
import ups_amazon_pb2

def send_msg(msg, socket):
    print("sending")
    print(msg)
    print("sending complete")
    string = msg.SerializeToString()
    data = []
    _VarintEncoder()(data.append, len(string), None)
    size = b''.join(data)
    socket.sendall(size + string)

def recv_connected(socket):
    data = b''
    while True:
        try:
            data += socket.recv(1)
            size = _DecodeVarint32(data, 0)[0]
            break
        except IndexError:
            pass
    string = socket.recv(size)
    UResponse = ups_world_pb2.UConnected()
    UResponse.ParseFromString(string)
    return UResponse

def recv_world_msg(socket):
    data = b''
    data += socket.recv(1)
    size = _DecodeVarint32(data, 0)[0]
    string = socket.recv(size)
    UResponse = ups_world_pb2.UResponses()
    UResponse.ParseFromString(string)
    return UResponse

def recv_amazon_msg(socket):
    data = b''
    data += socket.recv(1)
    size = _DecodeVarint32(data, 0)[0]
    string = socket.recv(size)
    UResponse = ups_amazon_pb2.AUCommands()
    UResponse.ParseFromString(string)
    return UResponse