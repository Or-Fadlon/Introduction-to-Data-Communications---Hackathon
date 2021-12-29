import socket
import struct

try:  # lab
    import getch as getch
except:  # pc
    import msvcrt as getch


class Client:
    def __init__(self, team_name):
        # TODO: make attributes private
        self.team_name = team_name
        self.is_alive = False
        self.local_ip = socket.gethostbyname(socket.gethostname())
        self.udp_socket = None
        self.udp_port = 13117
        self.udp_format = ">IBH"  # "IbH"
        self.server_ip = None
        self.tcp_socket = None
        self.tcp_port = 0  # TODO: what should be the value?
        self.buffer_size = 1024
        self.magic_cookie = 0xabcddcba
        self.message_type = 0x2

    def start(self):
        self.is_alive = True
        # open udp listener
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                                   1)  # TODO: change the SO_REUSEPORT was SO_REUSEADDR
        self.udp_socket.bind(("", self.udp_port))

        while self.is_alive:
            self.server_ip, self.tcp_port = self.__find_server()
            try:
                self.connect_to_server()
            except Exception as e:
                # TODO: handle
                print("Connection failed , reconnecting ...")
                continue
            self.__game()

    def stop(self):
        self.is_alive = False

    def __find_server(self):
        while self.is_alive:
            try:
                # wait for options
                data, address = self.udp_socket.recvfrom(self.buffer_size)
                message = struct.unpack(self.udp_format, data)
            except struct.error:
                continue
            if message[0] == self.magic_cookie and message[1] == self.message_type:
                print(f"Received offer from {address[0]}, attempting to connect...")
                return address[0], int(message[2])

    def connect_to_server(self):
        if not self.is_alive:
            raise Exception
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.connect((self.server_ip, self.tcp_port))

    def __game(self):
        self.__send_message(self.team_name + "\n")
        self.__receive_message()
        self.__send_message(self.__get_user_input())
        self.__receive_message()

    def __receive_message(self):
        while self.is_alive:
            try:
                message = self.tcp_socket.recv(self.buffer_size)
            except:
                print("Server disconnected, listening for offer requests...")
                return
            if not message:
                print("Server disconnected, listening for offer requests...")
                return
            print(message.decode())

    def __send_message(self, message):
        try:
            self.tcp_socket.send(message.encode())
        except:
            print("Server disconnected, listening for offer requests...")

    @staticmethod
    def __get_user_input():
        return str(getch.getch().decode())
