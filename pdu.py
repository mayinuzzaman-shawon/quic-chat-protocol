import json

# Define message types
MSG_TYPE_DATA = 0x00
MSG_TYPE_ACK = 0x01
MSG_TYPE_DATA_ACK = MSG_TYPE_DATA | MSG_TYPE_ACK

class Datagram:

    def __init__(self, mtype: int, msg: str, sz: int = 0, recipient: str = None):
        self.mtype = mtype
        self.msg = msg
        self.sz = len(self.msg)
        self.recipient = recipient
    
    # Function to convert the datagram object to JSON
    def to_json(self):
        return json.dumps(self.__dict__)

    # Function to create a datagram object from JSON
    @staticmethod
    def from_json(json_str):
        return Datagram(**json.loads(json_str))

    # Function to convert the datagram object to bytes
    def to_bytes(self):
        return json.dumps(self.__dict__).encode('utf-8')

    # Function to create a datagram object from bytes.
    @staticmethod
    def from_bytes(json_bytes):
        return Datagram(**json.loads(json_bytes.decode('utf-8')))
