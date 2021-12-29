import random

from MathGame.Client.Client import Client


def main():
    client = Client("Or" + str(random.randrange(0, 5)))
    client.start()


main()
