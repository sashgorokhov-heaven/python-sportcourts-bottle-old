import socket, pickle, struct, modules.utils

_struct_format = '!I'
_struct_len = struct.calcsize(_struct_format)


def _pack_data(data:object) -> bytes:
    data = pickle.dumps(data)
    size = len(data)
    return struct.pack(_struct_format, size) + data


def _unpack_data(sock:socket.socket) -> object:
    size = struct.unpack(_struct_format, sock.recv(_struct_len))[0]
    data = pickle.loads(sock.recv(size))
    return data


def _socket_factory():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Session:
    def __init__(self, sock:socket.socket, addr:tuple):
        self._sock = sock
        self._addr = addr
        self._stop = False
        self._header = _struct_format

    def addr(self):
        return self._addr

    def _recv(self):
        return _unpack_data(self._sock)

    def _send(self, data:object):
        self._sock.sendall(_pack_data(data))

    def send(self, data:object):
        self._send(data)

    def recieve(self):
        return self._recv()

    def sendrecv(self, data:object):
        self.send(data)
        return self.recieve()

    def close(self):
        try:
            self._sock.close()
        except:
            pass


class Server:
    def __init__(self, server_addr:tuple=('localhost', 12345)):
        self._server_addr = server_addr
        self._server_stop = False
        self._on_connection = lambda x: print('Connection', x._addr)
        self.BUFFER_SIZE = 1024

        self._server_sock = _socket_factory()
        self._server_sock.bind(self._server_addr)
        self._server_sock.listen(5)
        self._server_loop()

    def stop(self):
        self._server_stop = True

    @modules.utils.threaded
    def _server_loop(self):
        while not self._server_stop:
            try:
                sock, addr = self._server_sock.accept()
                modules.utils.threaded(self._on_connection)(Session(sock, addr))
            except Exception as e:
                print(e.__class__.__name__, e.args)
        self._server_sock.close()

    def set_on_connection(self, func):
        self._on_connection = func