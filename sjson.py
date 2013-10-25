import struct
import json
import socket
from sjson_utils import CMD, json_object_hook, json_default


class SJSON:

    def __init__(self, io=None, encoder=None, decoder=None):
        self.encoder = encoder or json.JSONEncoder(default=json_default)
        self.decoder = decoder or json.JSONDecoder(
            object_hook=json_object_hook)
        self.io = io or socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, address):
        """
        Method called by de clients for connect to servers
        """
        self.io.connect(address)

    def bind(self, address, listeners=5):
        """
        Method called by de servers for wait to the clients
        """
        self.io.bind(address)
        self.io.listen(listeners)
        clientsocket, address = self.io.accept()
        return SJSON(clientsocket), address

    def send(self, obj):
        """
        Encode the object into json, and send it prefixed with the length
        on binary.
        """
        encoded = self.encoder.encode(obj)
        length = struct.pack("I", len(encoded))
        msg = length + encoded
        self.io.send(msg)

    def recv(self, block=1):
        """
        Read the socket of jsons and transform it into a iterartor
        of objects
        """
        self.io.setblocking(block)
        received = True
        buf = ""
        while received:
            try:
                received = self.io.recv(1024)
            except socket.error:
                return
            buf += received
            while True:
                if len(buf) < 4:  # Needed for unpack number
                    break
                str_length = buf[:4]
                morebuf = buf[4:]
                length = struct.unpack("I", str_length)[0]
                if length > len(morebuf):  # Needed for decode object
                    break
                obj, buf = morebuf[:length], morebuf[length:]
                yield self.decoder.decode(obj)
        return

    def close(self):
        self.io.close()


if __name__ == "__main__":
    import random
    import os
    import time

    port = random.randint(5000, 9000)

    print socket.gethostname(), port

    if os.fork():
        # SERVER / EMITER
        server_sjson = SJSON()
        (client, address) = server_sjson.bind((socket.gethostname(), port))
        client.send({"hello": "world"})
        client.send(1j + 1)
        client.send(1)
        client.send(1.1)
        client.send("1")
        client.send(["1"])
        client.send(None)
        client.send(CMD("ACK"))
        client.send(CMD("ERROR"))
        client.send(CMD("WORKER"))
        client.send(CMD("END"))
        client.send(CMD("---"))  # == CMD("ERROR")
        client.close()
    else:
        # CLIENT / RECIVER
        time.sleep(.5)
        client_sjson = SJSON()
        client_sjson.connect((socket.gethostname(), port))
        for item in client_sjson.recv():
            print repr(item)
