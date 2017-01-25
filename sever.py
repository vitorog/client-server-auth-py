import ssl
import socket


class Server:
    def __init__(self, cert_filename, key_filename):
        print("Server instantiated")
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=cert_filename, keyfile=key_filename)

    def start(self, address, port):
        bind_socket = socket.socket()
        bind_socket.bind((address, port))
        bind_socket.listen(5)

        self.listen(bind_socket)

    def listen(self, bind_socket):
        print("Server listening")
        while True:
            new_socket, from_address = bind_socket.accept()
            conn_stream = self.context.wrap_socket(new_socket, server_side=True)
            try:
                self.authenticate(conn_stream)
            finally:
                conn_stream.shutdown(socket.SHUT_RDWR)
                conn_stream.close()

    def authenticate(self, conn_stream):
        data = conn_stream.recv(1024)
        print("Received data")
        print(data)
        while data:
            data = conn_stream.recv(1024)

if __name__ == '__main__':
    server = Server("server.crt", "server.key")
    server.start('localhost', 9000)
