import socket
import struct
import threading
import time
from MathGame.Server.Player import Player
from MathGame.Server.Game import Game


class Server:
    def __init__(self):
        # TODO: make attributes private
        self.is_alive = False
        self.is_broadcasting = False
        self.local_ip = socket.gethostbyname(socket.gethostname())
        self.udp_socket = None
        self.udp_ip = "255.255.255.255"
        self.udp_port = 13117
        self.udp_format = ">IBH"  # "IbH"
        self.tcp_socket = None
        self.tcp_port = 55566  # TODO: what should be the value?
        self.buffer_size = 1024
        self.magic_cookie = 0xabcddcba
        self.message_type = 0x2

    def start(self):
        self.is_alive = True
        # open udp connection
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # open tcp connection
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.bind(("", self.tcp_port))  # TODO: "" was self.local_ip
        self.tcp_socket.settimeout(10)  # TODO: need it?
        self.tcp_socket.listen()

        print("Server started, listening on IP address " + self.local_ip)
        # start strategy
        self.__strategy()

    def __start_broadcast(self):
        self.is_broadcasting = True
        threading.Thread(target=self.__send_broadcast).start()

    def __send_broadcast(self):
        message = struct.pack(self.udp_format, self.magic_cookie, self.message_type, self.tcp_port)
        while self.is_broadcasting:
            self.udp_socket.sendto(message, (self.udp_ip, self.udp_port))
            time.sleep(1)

    def __stop_broadcast(self):
        self.is_broadcasting = False

    def stop(self):
        self.is_alive = False
        self.__stop_broadcast()
        # kill tcp
        self.tcp_socket.close()
        # Kill UDP
        self.udp_socket.close()

    def __strategy(self):
        while self.is_alive:
            # start sending udp broadcast messages
            self.__start_broadcast()
            player1 = None
            player2 = None
            # wait for tcp connections
            # someone has connected
            while True:
                try:
                    new_client1 = self.tcp_socket.accept()  # (connection socket, address)
                    name1 = new_client1[0].recv(self.buffer_size).decode()
                    player1 = Player(new_client1[0], new_client1[1], name1)
                    break
                except socket.timeout:
                    if not self.is_alive:
                        break
            # someone has connected
            while True:
                try:
                    new_client2 = self.tcp_socket.accept()  # (connection socket, address)
                    name2 = new_client2[0].recv(self.buffer_size).decode()
                    player2 = Player(new_client2[0], new_client2[1], name2)
                    break
                except socket.timeout:
                    if not self.is_alive:
                        break

            if player1 and player2:
                # stop broadcast
                self.__stop_broadcast()
                # start strategy game
                Game(player1, player2)