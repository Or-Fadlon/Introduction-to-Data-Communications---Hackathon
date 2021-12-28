import random
import threading
import time
import socket


class Game:
    questions = {"1+1": 2, "2+2": 4, "3+3": 6, "4+4": 8}

    def __init__(self, player1, player2):
        self.__finish = False
        question = self.__generate_question()
        self.__question = question[0]
        self.__answer = question[1]
        self.__player1 = player1
        self.__player2 = player2

        self.__thread = threading.Thread(target=self.__game)
        self.__thread.start()

    @staticmethod
    def __generate_question():
        rand = random.randrange(0, len(Game.questions))
        key = Game.questions.keys()[rand]
        return key, Game.questions[key]

    def get_thread(self):
        return self.__thread

    def __game(self):
        # send problem to the two client
        self.__send_message_to_players(self.__get_message("begin") + self.__question + "?\n")
        # wait 10 seconds
        time.sleep(10)
        # get answer
        # two threads,each for each player
        response1 = []
        response2 = []
        t1 = threading.Thread(target=Game.__handle_player_question_answer, args=(self.__player1, response1))
        t2 = threading.Thread(target=Game.__handle_player_question_answer, args=(self.__player2, response2))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # set result
        self.__send_message_to_players(self.__get_message("over") + self.__answer + "!\n\n")

        if response1[0] == self.__answer and response2[0] != self.__answer:
            winner = self.__player1.get_name()
        elif response1[0] != self.__answer and response2[0] == self.__answer:
            winner = self.__player2.get_name()
        elif response1[0] == self.__answer and response2[0] == self.__answer:
            if response1[1] < response2[1]:
                winner = self.__player1.get_name()
            elif response1[1] > response2[1]:
                winner = self.__player2.get_name()
            else:
                winner = None
        else:
            winner = None

        if winner is None:
            self.__send_message_to_players(self.__get_message("draw"))
        else:
            self.__send_message_to_players(self.__get_message("win") + winner)

        # close game
        self.__finish_game()

    def __finish_game(self):
        self.__finish = True
        self.__player1.kill()
        self.__player2.kill()
        print("Game over, sending out offer requests...")

    def __handle_player_question_answer(self, player, response):
        player.get_sockt.settimeout(10)
        player.get_sockt.send(self.__get_message("question") + self.__question + "? ")
        start = time.localtime()
        try:
            ans = player.get_sockt.recv(1024)
        except socket.timeout:
            ans = float("-inf")
        end = time.localtime()
        response.append(ans)
        response.append(end - start)

    def __send_message_to_players(self, message):
        self.__player1.get_sockt.send(message)
        self.__player2.get_sockt.send(message)

    def __get_message(self, message_name):
        if message_name == "begin":
            return "Welcome to \"Yossi's-army\" team!\n" \
                   "We will play Quick Maths.\n" \
                   "Player 1: {name1}\n" \
                   "Player 2: {name2}\n" \
                   "==\n" \
                .format(name1=self.__player1.get_name(), name2=self.__player2.get_name())
        if message_name == "question":
            return "Please answer the following question as fast as you can:\n" \
                   "How much is "
        if message_name == "over":
            return "Game over!\n" \
                   "The correct answer was "
        if message_name == "draw":
            return "It's a Draw!"
        if message_name == "win":
            return "Congratulations to the winner: "
