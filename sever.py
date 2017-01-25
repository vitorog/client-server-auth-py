import ssl
import socket
import json


class Server:
    def __init__(self, cert_filename, key_filename):
        print("Server instantiated")
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=cert_filename, keyfile=key_filename)
        self.server_socket = None

    def start(self, address, port):
        bind_socket = socket.socket()
        bind_socket.bind((address, port))
        bind_socket.listen(5)

        self.listen(bind_socket)

    def listen(self, bind_socket):
        print("Server listening")
        while True:
            new_socket, from_address = bind_socket.accept()
            self.server_socket = self.context.wrap_socket(new_socket, server_side=True)
            try:
                self.check_messages()
            except ConnectionResetError as e:
                print("Caught exception: " + str(e))
                pass
            finally:
                self.close_connection()

    def close_connection(self):
        try:
            self.server_socket.shutdown(socket.SHUT_RDWR)
            self.server_socket.close()
        except OSError:
            pass

    def check_messages(self):
        data = self.server_socket.recv(1024)
        while True:
            if data:
                print("Received message")
                self.authenticate(data)
            else:
                break
            data = self.server_socket.recv(1024)

    def authenticate(self, data):
        json_message = json.loads(data.decode('utf-8'))
        if self.validate(json_message):
            if self.valid_credentials(json_message):
                self.send_login_message("SUCCESS")
            else:
                self.send_login_message("FAILED")

    def valid_credentials(self, json_message):
        # Actual user and password validation should go here
        return json_message['username'] == 'myuser' and json_message['password'] == 'mypassword'

    def send_login_message(self, status):
        login_response = '{"message_type":"LOGIN_RESPONSE", "status":"' + status + '"}'
        print("Login response is: " + login_response)
        self.server_socket.sendall(login_response.encode('utf-8'))

    def validate(self, json_message):
        if json_message['message_type'] == "LOGIN_MESSAGE":
            print("Valid message received: " + str(json_message))
            return True
        return False


if __name__ == '__main__':
    server = Server("server.crt", "server.key")
    server.start('localhost', 9003)
