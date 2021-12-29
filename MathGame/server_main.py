from MathGame.Server.Server import Server


def main():
    server = Server()
    server.start()
    # while input("Q for stop") != 'Q':
    #     continue
    server.stop()



main()
