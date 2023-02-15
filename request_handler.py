from Crypto.Cipher import AES
import helper
import struct
from response import Response, Response_Type

NAME_SIZE = 255
PUBLIC_KEY_SIZE = 160
CONTENT_SIZE_SIZE = 4
FILE_NAME_SIZE = 255
CLIENT_ID_SIZE = 16

def registration(request):
    pass

def send_public_key(request):
    client_id = request.header.code
    client_name, public_key = struct.unpack("<{}s{}s".format(NAME_SIZE, PUBLIC_KEY_SIZE), request.payload)
    query = """UPDATE clients SET PublicKey = {} where ID = {}""".format(public_key, client_id)
    helper.execute_query(query)
    AES_key = helper.create_AES_key(public_key)
    query = """UPDATE clients SET AES = {} where ID = {}""".format(AES_key, client_id)
    helper.execute_query(query)
    AES_key_size = len(AES_key)
    code = Response_Type.AES_CREATED
    payload = struct.pack("<{}s{}s".format(CLIENT_ID_SIZE,AES_key_size))
    response = Response(code, payload)
    packed_response = response.packed_response()
    return packed_response


def re_connect(request):
    cliend_id = request.Header["ClientID"]
    query = """SELECT AES FROM clients WHERE ID = {}""".format(cliend_id)
    replay = helper.execute_query(query)
    if replay == []:
        code = Response_Type.RE_CONNECT_REFUSED
        #todo send pack response
    else:
        AES_key = replay[0][0]
        code = Response_Type.RE_CONNECT
        # todo send pack response

def send_file(request):
    content_size = request.payload[0 : 4]
    file_name = request.payload[4 : 260]
    messageContent = request.payload[260 :]


def correct_CRC(request):
    pass

def incorrect_CRC(request):
    pass

def incorrect_CRC_fourth(request):
    pass