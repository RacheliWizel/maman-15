from Crypto.Cipher import AES
import helper

AES_CREATED = 2102
RE_CONNECT_REFUSED = 2106
RE_CONNECT = 2105

def registration(request):
    pass

def send_public_key(request):
    client_id = request.Header["ClientID"]
    public_key = request.payload[256 : 417]
    query = """UPDATE clients SET PublicKey = {} where ID = {}""".format(public_key, client_id)
    helper.execute_query(query)
    AES_key = helper.create_AES_key(public_key)
    query = """UPDATE clients SET AES = {} where ID = {}""".format(AES_key, client_id)
    helper.execute_query(query)
    code = AES_CREATED
    payload = {client_id : 16,
               AES_key : '-'}
    helper.create_response(code, payload)

def re_connect(request):
    cliend_id = request.Header["ClientID"]
    query = """SELECT AES FROM clients WHERE ID = {}""".format(cliend_id)
    replay = helper.execute_query(query)
    if replay == []:
        code = RE_CONNECT_REFUSED
        payload = {cliend_id : 16}
        helper.create_response(code, payload)
    else:
        AES_key = replay[0][0]
        code = RE_CONNECT
        payload = {cliend_id : 16,
                   AES_key : '-'}
        helper.create_response(code, payload)

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