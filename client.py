import ssl
import socket
import json


class Client:
    def __init__(self, cert_file_name):
        print("Client instantiated")

        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.check_hostname = True
        self.context.load_verify_locations(cert_file_name)
        self.socket = None

    def connect(self, address, port, hostname):
        self.socket = self.context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
        self.socket.connect((address, port))

    def login(self, username, password):
        print('Login executed')
        self.socket.sendall(self.build_login_message(username, password))
        print("Waiting for response...")
        if self.handle_response():
            print('Login Success!')
        else:
            print('Login Failed!')

    def handle_response(self):
        try:
            data = self.socket.recv(1024)
            while True:
                if data:
                    json_message = json.loads(data.decode('utf-8'))
                    if self.validate(json_message):
                        return self.get_status(json_message)
                else:
                    break
                data = self.socket.recv(1024)
        finally:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()

    def build_login_message(self, username, password):
        login_message = '{"message_type":"LOGIN_MESSAGE", "username":"' + username + '", "password":"' + password + '"}'
        print("Login request is: " + login_message)
        return login_message.encode('utf-8')

    def validate(self, json_message):
        return json_message['message_type'] == 'LOGIN_RESPONSE'

    def get_status(self, json_message):
        return json_message['status'] == 'SUCCESS'


if __name__ == '__main__':
    client = Client('server.crt')
    client.connect('localhost', 9003, 'localhost')
    client.login("myuser", "mypassword")