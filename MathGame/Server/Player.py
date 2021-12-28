class Player:

    def __init__(self, socket, address, name):
        self.__socket = socket
        self.__address = address
        self.__name = name

    def get_socket(self):
        return self.__socket

    def get_address(self):
        return self.__address

    def get_name(self):
        return self.__name

    def kill(self):
        self.__socket.close()
