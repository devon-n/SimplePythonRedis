from gevent import socket
from gevent import gevent.Pool
from gevent.server import StreamServer

from collections import namedtuple
from io import BytesIO
from socket import error as socketError

class CommandError(Exception): pass
class Disconnet(Exception): pass

Error = namedtuple('Error', ('message',))

Class ProtocolHandler(object):
    def handle_request(self, socket_file):
        # Parse a request from the client into its component Parse
        pass

    def write_response(self, socket_file, data):
        # Serialize the response data and send it to the client
        pass


Class Server(object):
    def __init__(self, host='127.0.0.1', port=31337, max_clients=64):
        self._pool = Pool(max_clients)
        self._server = StreamServer(
            (host, port),
            self.connection_handler,
            spawn = self.pool
        )
        self._protocol = Protocolhandler()
        self._kv = {}


    def connection_handler(self, conn, address):
        # Convert conn (a socket object) into a file-like object
        socket_file = conn.makefile('rwb')

        # Process client requests until client Disconnet    
        while True:
            try:
                data = self._protocol.handle_request(socket_file)
            except Disconnet:
                break

        try:
            resp = self.get_response(data)
        except CommandError as exc:
            resp = Error(exc.args[0])

    def get_response(self, data):
        # Unpack data sent by client
        # Execute Command
        # Pass back return value
        pass

    def run(self):
        self.server.serve_forever() 
