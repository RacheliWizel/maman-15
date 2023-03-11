import request_handler
import struct
from enum import Enum

# Define constants for header and client ID size
HEADER_SIZE = 23
CLIENT_ID_SIZE = 16

# Define enum for request type codes
class request_type(Enum):
    REGISTRATION = 1100
    SEND_PUBLIC_KEY = 1101
    RE_CONNECT = 1102
    SEND_FILE = 1103
    CORRECT_CRC = 1104
    INCORRECT_CRC = 1105
    INCORRECT_CRC_FOURTH = 1106

# Define error message
ERROR = "UNVALID CODE"

# Define a class to represent the header of a request
class Request_Header():
    def __init__(self, clientID, version, code, payloadSize):
        self.clientID = clientID
        self.version = version
        self.code = code
        self.payloadSize = payloadSize

# Define a class to represent a request
class Request:

    def __init__(self, buffer):
        # Unpack the buffer to get the client ID, version, request code, and payload size
        client_id, version, code , payload_size = struct.unpack("<{}sBHL".format(CLIENT_ID_SIZE), buffer)
        # Create a new Request_Header object with the header information
        self.header = Request_Header(client_id, version, code , payload_size)
        # Extract the payload from the buffer
        self.payload = buffer[HEADER_SIZE : HEADER_SIZE + payload_size]

    def handel_request(self):
        # Set default response to error message
        response = ERROR
        # Determine the request code and call the appropriate function from request_handler module
        if self.header.code == request_type.REGISTRATION:
            response = request_handler.registration(self)
        elif self.header.code == request_type.SEND_PUBLIC_KEY:
            response = request_handler.send_public_key(self)
        elif self.header.code == request_type.RE_CONNECT:
            response = request_handler.re_connect(self)
        elif self.header.code == request_type.SEND_FILE:
            response = request_handler.send_file(self)
        elif self.header.code == request_type.CORRECT_CRC:
            response = request_handler.correct_CRC(self)
        elif self.header.code == request_type.INCORRECT_CRC:
            response = 'no message'
        elif self.header.code == request_type.INCORRECT_CRC_FOURTH:
            response = request_handler.incorrect_CRC_fourth(self)
        # Return the response from the appropriate function
        return response