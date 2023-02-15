import request_handler

ERROR = "UNVALID CODE"

class Request:
    Header = {"ClientID" : 0,
              "Version" : 0,
              "Code" : 0,
              "PayloadSize": 0}
    payload = ""

    def __init__(self, buffer):
        self.Header["ClientID"] = buffer[0 : 17]
        self.Header["Version"] = buffer[17 : 18]
        self.Header["Code"] = buffer[18 : 20]
        self.Header["PayloadSize"] = buffer[20 : 24]
        self.payload = buffer[24 :]

    def handel_request(self):
        response = ERROR
        if self.Header["Code"] == 1100:
            response = request_handler.registration(self)
        elif self.Header["Code"] == 1101:
            response = request_handler.send_public_key(self)
        elif self.Header["Code"] == 1102:
            response = request_handler.re_connect(self)
        elif self.Header["Code"] == 1103:
            response = request_handler.send_file(self)
        elif self.Header["Code"] == 1104:
            response = request_handler.correct_CRC(self)
        elif self.Header["Code"] == 1105:
            response =  request_handler.incorrect_CRC(self)
        elif self.Header["Code"] == 1106:
            response = request_handler.incorrect_CRC_fourth(self)
        return response



