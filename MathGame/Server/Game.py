import queue
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

        self.__game()
        # self.__thread = threading.Thread(target=self.__game)
        # self.__thread.start()

    @staticmethod
    def __generate_question():
        rand = random.randrange(0, len(Game.questions))
        key = list(Game.questions.keys())[rand]
        return key, Game.questions[key]

    def __game(self):
        # wait 10 seconds
        time.sleep(10)
        # get answer
        # two threads,each for each player
        response1 = queue.Queue()
        response2 = queue.Queue()
        t1 = threading.Thread(target=Game.__handle_player_question_answer, args=[self, self.__player1, response1])
        t2 = threading.Thread(target=Game.__handle_player_question_answer, args=[self, self.__player2, response2])
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        response1 = response1.get()
        response2 = response2.get()

        # set result
        message = self.__get_message("over") + str(self.__answer) + "!\n\n"

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
            message += self.__get_message("draw")
        else:
            message += self.__get_message("win") + winner

        # send results
        self.__send_message_to_players(message)

        # close game
        self.__finish_game()

    def __finish_game(self):
        self.__finish = True
        self.__player1.kill()
        self.__player2.kill()
        print("Game over, sending out offer requests...")

    def __handle_player_question_answer(self, player, response):
        player.get_socket().settimeout(10)
        message = self.__get_message("icon") + self.__get_message("begin") + self.__question + "? \n"
        player.get_socket().send(message.encode())
        start = time.time()
        try:
            ans = player.get_socket().recv(1024)
            ans = ans.decode()
            ans = int(ans)
        except socket.timeout:
            ans = float("-inf")
        end = time.time()
        return_tuple = (ans, end - start)
        response.put(return_tuple)

    def __send_message_to_players(self, message):
        self.__player1.get_socket().send(message.encode())
        self.__player2.get_socket().send(message.encode())

    def __get_message(self, message_name):
        if message_name == "icon":
            return " __     __                      _   _ \n" \
                   " \ \   / /                     (_) ( ) \n" \
                   "  \ \_/ /    ___    ___   ___   _  |/   ___   ______    __ _   _ __   _ __ ___    _   _ \n" \
                   "   \   /    / _ \  / __| / __| | |     / __| |______|  / _` | | '__| | '_ ` _ \  | | | | \n" \
                   "    | |    | (_) | \__ \ \__ \ | |     \__ \          | (_| | | |    | | | | | | | |_| | \n" \
                   "    |_|     \___/  |___/ |___/ |_|     |___/           \__,_| |_|    |_| |_| |_|  \__, | \n" \
                   "                                                                                   __/ | \n" \
                   "                                                                                  |___/  \n" \
                   " \n" \
                   " +--^----------,--------,-----,--------^-, \n" \
                   " | |||||||||   `--------'     |          O \n" \
                   " `+---------------------------^----------| \n" \
                   "   `\_,---------,---------,--------------' \n" \
                   "     / XXXXXX /'|       /' \n" \
                   "    / XXXXXX /  `\    /' \n" \
                   "   / XXXXXX /`-------' \n" \
                   "  / XXXXXX / \n" \
                   " / XXXXXX / \n" \
                   "(________( \n" \
                   "`------' \n\n"
        if message_name == "begin":
            return "Welcome to \"Yossi's-army\" team!\n" \
                   "We will play Quick Maths.\n" \
                   "Player 1: {name1}\n" \
                   "Player 2: {name2}\n" \
                   "==\n" \
                   "Please answer the following question as fast as you can:\n" \
                   "How much is " \
                .format(name1=self.__player1.get_name(), name2=self.__player2.get_name())
        if message_name == "over":
            return "Game over!\n" \
                   "The correct answer was "
        if message_name == "draw":
            return "It's a Draw!"
        if message_name == "win":
            return "Congratulations to the winner: "
