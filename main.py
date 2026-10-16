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

    def __init__(self):
        self.handlers = {
            '+': self.handle_simple_string,
            '-': self.handle_error,
            ':': self.handle_integer,
            '$': self.handle_string,
            '*': self.handle_array,
            '%': self.handle_dict
        }

    def handle_request(self, socket_file):
        # Parse a request from the client into its component
        first_byte = socket_file.read(1)
        if not first_byte:
            raise Disconnet

        try:
            return self.handlers[first_byte](socket_file)

        except KeyError:
            raise CommandError('bad request')

    def handle_simple_string(self, socket_file):
        return socket_file.readline().rstrip('/r/n')

    def handle_error(self, socket_file):
        return Error(self.handle_simple_string(socket_file))

    def handle_integer(self, socket_file):
        return int(self.handle_simple_string(socket_file))

    def handle_string(self, socket_file):
        length = int(self.handle_simple_string(socket_file))
        if length = -1:
            return None
        length += 2
        return socket_file.read(length)[:-2]

    def handle_array(self, socket_file):
        num_elements = self.handle_integer(socket_file)
        return [self.handle_request(socket_file) for _ in range(num_elements)]

    def handle_dict(self, socket_file):
        num_items = self.handle_integer(socket_file)
        elements = [self.handle_request(socket_file) for _ in range (num_items * 2)]
        return dict(zip(elements[::2], elements[1::2]))

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
