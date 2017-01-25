import ssl
import socket


class Client:
    def __init__(self, cert_file_name):
        print("Client instantiated")

        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.check_hostname = True
        self.context.load_verify_locations(cert_file_name)
        # For testing purposes
        self.context.check_hostname = False

    def connect(self, address, port, hostname):
        conn = self.context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
        conn.connect((address, port))

    def login(self, username, password):
        print('Login executed')


if __name__ == '__main__':
    client = Client('server.crt')
    client.connect('localhost', 9000, 'MyServer')
    client.login("myuser", "mypassword")