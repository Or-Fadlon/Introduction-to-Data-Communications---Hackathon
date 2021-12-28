import socket
import struct
import _thread as thread
import time
from MathGame.Server.Player import Player


class Server:
    def __init__(self):
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
        self.tcp_socket.listen(1)

        print("Server started, listening on IP address " + self.local_ip)
        # start sending udp broadcast messages
        self.send_broadcast()
        # start strategy
        self.__strategy()

    def send_broadcast(self):
        message = struct.pack(self.udp_format, self.magic_cookie, self.message_type, self.tcp_port)
        while self.is_alive:
            self.udp_socket.sendto(message, (self.udp_ip, self.udp_port))
            time.sleep(5)

    def stop(self):
        self.is_alive = False
        # kill tcp
        # Kill UDP

    def __strategy(self):
        while self.is_alive:
            # wait for tcp connections
            # someone has connected
            # player1 = Player(self.tcp_socket.accept(),)
            while True:
                player1 = self.tcp_socket.accept()  # (connection socket, address)
                if self.__check_player(player1):
                    break
            # someone has connected
            while True:
                player2 = self.tcp_socket.accept()  # (connection socket, address)
                if self.__check_player(player2):
                    break
            self.__game(player1, player2)
            # start strategy game

    def __check_player(self, player):
        pass

    def __game(self, player1, player2):
        player1_socket = player1[0]
        player2_socket = player2[0]
        # send problem to the two client
        math_problem = "1+1=2"
        self.__send_message_to_players(math_problem, player1_socket, player2_socket)
        # get answer
        # two threads,each for each player
        # thread.start_new_thread()
        player1_answer = player1_socket.recv(1024)
        player2_answer = player2_socket.recv(1024)
        # set result
        self.__send_message_to_players("the result is", player1_socket, player2_socket)  # TODO
        self.__send_message_to_players("thank you for playing with us", player1_socket, player2_socket)
        # close game
        player1_socket.close()
        player2_socket.close()

    def __send_message_to_players(self, message, player1_socket, player2_socket):
        player1_socket.send(message)
        player2_socket.send(message)
