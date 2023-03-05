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
    try:
        client_id = request.header.code
        client_name, public_key = struct.unpack("<{}s{}s".format(NAME_SIZE, PUBLIC_KEY_SIZE), request.payload)
        query = """UPDATE clients SET PublicKey = {} where ID = {}""".format(public_key, client_id)
        helper.execute_query(query)
        AES_key, decrypted_AES_key = helper.create_AES_key(public_key)
        query = """UPDATE clients SET AES = {} where ID = {}""".format(AES_key, client_id)
        helper.execute_query(query)
        decrypted_AES_key_size = len(decrypted_AES_key)
        code = Response_Type.AES_CREATED
        payload = struct.pack("<{}s{}s".format(CLIENT_ID_SIZE,decrypted_AES_key_size),client_id,decrypted_AES_key)
        response = Response(code, payload)
        packed_response = response.packed_response()
        return packed_response
    except:
        packed_response = general_error()
        return  packed_response

def re_connect(request):
    try:
        client_id = request.Header.clientID
        query = """SELECT AES FROM clients WHERE ID = {}""".format(client_id)
        replay = helper.execute_query(query)
        if replay == []:
            code = Response_Type.RE_CONNECT_REFUSED
            payload = struct.pack("<{}s".format(CLIENT_ID_SIZE), client_id)
            response = Response(code, payload)
            packed_response = response.packed_response()
            return packed_response
        else:
            AES_key = replay[0][0]
            AES_key_size = len(AES_key)
            code = Response_Type.RE_CONNECT
            payload = struct.pack("<{}s{}s".format(CLIENT_ID_SIZE, AES_key_size), client_id, AES_key)
            response = Response(code, payload)
            packed_response = response.packed_response()
            return packed_response
    except:
        packed_response = general_error()
        return packed_response


def send_file(request):
    try:
        client_id = request.header.clientID
        content_size = struct.unpack("<L", request.payload[:CONTENT_SIZE_SIZE])
        left_payload = request.payload[CONTENT_SIZE_SIZE:]
        file_name, message_content = struct.unpack("<{}s{}s".format(FILE_NAME_SIZE, content_size), left_payload)
        query = """SELECT AES from clients where ID = {} """.format(client_id)
        AES_key = helper.execute_query(query)[0][0]
        decrypeted_file_content = helper.decrypet_file(message_content, AES_key)
        query = """UPDATE files SET FileName = {} PathName = {} Verified = false where ID = {}""".format(client_id + '_' + file_name , "./files" ,client_id)
        helper.execute_query(query)
        f = open("./files/{}".format(client_id + '_' + file_name), "a")
        f.write(decrypeted_file_content)
        f.close()
        file_sum = helper.check_file_sum(decrypeted_file_content)
        code = Response_Type.CORRECT_AND_SEND_CRC
        payload = struct.pack("<{}sL{}sL".format(CLIENT_ID_SIZE, FILE_NAME_SIZE), client_id, content_size, file_name, file_sum)
        response = Response(code, payload)
        packed_response = response.packed_response()
        return packed_response
    except:
        packed_response = general_error()
        return packed_response

def correct_CRC(request):
    try:
        client_id = request.header.clientID
        file_name = struct.unpack("<{}s".format(FILE_NAME_SIZE), request.payload)
        query = """UPDATE files SET Verified = true where ID = {} and FileName = {}""".format( client_id , client_id + '_' + file_name )
        helper.execute_query(query)
        code = Response_Type.RECEIVED_MESSAGE
        payload = struct.pack("<{}s".format(CLIENT_ID_SIZE), client_id)
        response = Response(code, payload)
        packed_response = response.packed_response()
        return packed_response
    except:
        packed_response = general_error()
        return packed_response


def incorrect_CRC_fourth(request):
    try:
        client_id = request.header.clientID
        file_name = struct.unpack("<{}s".format(FILE_NAME_SIZE), request.payload)
        code = Response_Type.RECEIVED_MESSAGE
        payload = struct.pack("<{}s".format(CLIENT_ID_SIZE), client_id)
        response = Response(code, payload)
        packed_response = response.packed_response()
        return packed_response
    except:
        packed_response = general_error()
        return packed_response

def general_error():
    code = Response_Type.ERROR
    response = Response(code, '')
    packed_response = response.packed_response()
    return packed_response
