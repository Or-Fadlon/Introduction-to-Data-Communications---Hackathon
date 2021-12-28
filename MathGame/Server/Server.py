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
        self.local_ip = socket.gethostbyname(socket.gethostname())
        self.udp_socket = None
        self.udp_ip = "255.255.255.255"
        self.udp_port = 13117
        self.udp_format = "IbH"
        self.tcp_socket = None
        self.tcp_port = 0  # TODO: what should be the value?
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
        self.tcp_socket.bind((self.local_ip, self.tcp_port))
        self.tcp_socket.settimeout(10)  # TODO: need it?
        self.tcp_socket.listen()

        print("Server started, listening on IP address " + self.local_ip)
        # start sending udp broadcast messages
        threading.Thread(target=self.send_broadcast).start()
        # start strategy
        self.__strategy()

    def send_broadcast(self):
        message = struct.pack(self.udp_format, self.magic_cookie, self.message_type, self.tcp_port)
        while self.is_alive:
            self.udp_socket.sendto(message, (self.udp_ip, self.udp_port))
            time.sleep(1)

    def stop(self):
        self.is_alive = False
        # kill tcp
        # Kill UDP

    def __strategy(self):
        while self.is_alive:
            player1 = None
            player2 = None
            # wait for tcp connections
            # someone has connected
            while True:
                try:
                    new_client1 = self.tcp_socket.accept()  # (connection socket, address)
                    if self.__check_player(new_client1):
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
                    if self.__check_player(new_client2):
                        name2 = new_client2[0].recv(self.buffer_size).decode()
                        player2 = Player(new_client2[0], new_client2[1], name2)
                        break
                except socket.timeout:
                    if not self.is_alive:
                        break
            if player1 and player2:
                # start strategy game
                Game(player1, player2)

    def __check_player(self, player):
        # TODO: add logic
        return True
