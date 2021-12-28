from socket import *
import socket


class Server:
    def __init__(self):
        self.local_ip = None
        self.server_port = 12000
        self.udp_socket = None
        self.tcp_socket = None
        self.is_alive = False

    def start(self):
        self.is_alive = True
        # open udp connection
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.udp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.local_ip = socket.gethostbyname(socket.gethostname())
        print("Server started,listening on IP address" + self.local_ip)
        # open tcp connection
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_socket.bind(('', self.server_port))
        self.tcp_socket.listen(1)
        # start sending udp broadcast messages
        self.udp_socket.sendto("This is a test".encode(), ('255.255.255.255', 54545))
        # start strategy
        self.__strategy()

    def stop(self):
        self.is_alive = False
        # kill tcp
        # Kill UDP

    def __strategy(self):
        while self.is_alive:
            # wait for tcp connections
            # someone has connected
            player1 = self.tcp_socket.accept()  # (connection socket, address)
            # someone has connected
            player2 = self.tcp_socket.accept()  # (connection socket, address)
            self.__game(player1, player2)
            # start strategy game

    def __game(self, player1, player2):
        player1_socket = player1[0]
        player2_socket = player2[0]
        # send problem to the two client
        math_problem = "1+1=2"
        self.__send_message_to_players(math_problem, player1_socket, player2_socket)
        # get answer
        # two threads,each for each player
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
