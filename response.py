from enum import Enum
import struct

SERVER_VERSION = 3
HEADER_SIZE = 7

class Response_Type(Enum):
    REGISTRATION_SUCCESS = 2100
    REGISTRATION_FAILED = 2101
    AES_CREATED = 2102
    CORRECT_AND_SEND_CRC = 2103
    RECEIVED_MESSAGE = 2104
    RE_CONNECT = 2105
    RE_CONNECT_REFUSED = 2106
    ERROR = 2107

class Response_Header:
    def __init__(self, code, payload_size, version = SERVER_VERSION):
        self.version = version
        self.code = code
        self.payload_size = payload_size

    def pack_header(self):
        packed_header = struct.pack("<BHL",self.version, self.code, self.payload_size)
        return packed_header

class Response:
    def __init__(self, code, payload):
        self.header = Response_Header(code, len(payload))
        self.packed_header = self.header.pack_header()
        self.payload = payload

    def packed_response(self):
        return self.packed_header + self.payload




