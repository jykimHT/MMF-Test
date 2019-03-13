import socket
from struct import *
import json
import traceback


def recv_data(sock):
    try:
        length = int.from_bytes(sock.recv(4), byteorder='big')
        print("length : %d" % length)

        if length == 0:
            return 'No Data'

        response = bytes()
        data = sock.recv(length)
        response += data

        header = response[0:24]
        print_header(header)
        body = "{0}".format(response.decode('utf-8')[24:])
        print("body : " + body)
    except socket.timeout as e:
        print(traceback.format_exc())
        sock.close()
        return "Exception : %s" % e
    return body


def create_request(pincode='00000000', type=1, sub=7, body=''):
    pincode = pincode.encode('utf-8')
    type = pack(">I", type)
    sub = pack(">I", sub)
    src = pack(">H", 1)
    dest = pack(">H", 3)
    error = pack(">B", 0)
    reserved = b'\x00\x00\x00'
    body = body.encode('utf-8')

    request = pincode + type + sub + src + dest + error + reserved + body
    length = pack(">I", len(request))
    request = length + request

    return request


def login(sock, mmf_type, id, pw, uuid):
    if mmf_type == "이마주":
        login_sub = 7
        login_body = '{"id":"' + id + '","pw":"' + pw + '","uuid":"' + uuid + '"}'
    elif mmf_type == "대림":
        login_sub = 5
        login_body = '{"id":"' + id + '","pw":"' + pw + '","UUID":"' + uuid + '"}'
    request = create_request(sub=login_sub, body=login_body)
    sock.send(request)

    response = recv_data(sock)
    return response


def get_pincode(mmf_type, data):
    pincode = ''
    try:
        data_json = json.loads(data)
    except ValueError:
        data = data[:-1]
        try:
            data_json = json.loads(data)
        except ValueError:
            return ''

    if mmf_type == "이마주":
        pincode = data_json['loginpin']
    elif mmf_type == "대림":
        pincode = data_json['certpin']
    return pincode


def send_message(request_info):
    mmf_type = request_info.get_mmf_type()
    ip = request_info.get_ip()
    port = request_info.get_port()
    id = request_info.get_id()
    pw = request_info.get_password()
    uuid = request_info.get_uuid()
    type = request_info.get_type()
    sub = request_info.get_sub_type()
    body = request_info.get_body()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)
    try:
        sock.connect(server_address)
    except socket.error as e:
        print(traceback.format_exc())
        sock.close()
        return "Exception : %s" % e
    sock.settimeout(5)

    print('*******************************')
    print("Get pincode for request\n")
    response = login(sock, mmf_type, id, pw, uuid)

    if response != '':
        pincode = get_pincode(mmf_type, response)
        if pincode == '':
            return 'Can not get pincode'
    else:
        return 'Login fail'

    print("pincode : " + pincode)

    print('*******************************')
    print('Main Request\n')

    request = create_request(pincode=pincode, type=type, sub=sub, body=body)
    sock.send(request)

    response = recv_data(sock)
    sock.close()

    return response


def print_header(header):
    pincode = header[0:8]
    type = header[8:12]
    sub_type = header[12:16]
    src = header[16:18]
    dest = header[18:20]
    error = header[20]

    print("header : ", end='[')
    print("pincode : " + pincode.decode('utf-8'), end=', ')
    print("type : %d" % int.from_bytes(type, "big"), end=', ')
    print("subType : %d" % int.from_bytes(sub_type, "big"), end=', ')
    print("src : %d" % unpack('>H', src)[0], end=', ')
    print("dest : %d" % unpack('>H', dest)[0], end=', ')
    print("error : %x" % error, end=']\n')


class RequestInfo:
    __mmf_type = ''
    __ip = ''
    __port = 0
    __id = ''
    __password = ''
    __uuid = ''
    __type = 0
    __sub_type = 0
    __body = ''

    def __init__(self, mmf_type, ip, port, id, password, uuid, type, sub_type, body):
        self.__mmf_type = mmf_type
        self.__ip = ip
        self.__port = port
        self.__id = id
        self.__password = password
        self.__uuid = uuid
        self.__type = type
        self.__sub_type = sub_type
        self.__body = body

    def get_mmf_type(self):
        return self.__mmf_type

    def get_ip(self):
        return self.__ip

    def get_port(self):
        return self.__port

    def get_id(self):
        return self.__id

    def get_password(self):
        return self.__password

    def get_uuid(self):
        return self.__uuid

    def get_type(self):
        return self.__type

    def get_sub_type(self):
        return self.__sub_type

    def get_body(self):
        return self.__body
