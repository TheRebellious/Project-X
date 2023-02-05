import json
import socket
import sys
import threading
from time import sleep
import arcade


class Server:
    clientsockets = []
    clientPositions = []

    def __init__(self, Host: bool) -> None:
        print("INIT")
        self.host = Host

    def start(self):
        print("START")
        if self.host:
            self.hostGame()
        else:
            self.joinGame()

    def accept(self):
        while True:
            try:
                if not arcade.get_window():
                    if self.host:
                        self.server.close()
                        print("Server closed!")
                    else:
                        self.clientsocket.close()
                        print("Client closed!")
                    exit()
                # print("Waiting for connection...")
                self.clientsockets.insert(0, self.server.accept())
                self.clientPositions.insert(0, [0, 0])
                print(
                    f"Connection from {self.clientsockets[0][0]} has been established!")
            except:
                pass

    def hostGame(self):
        print("HOST")
        try:
            print("Starting server...")
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(("", 1234))
            print("Server started!")
            self.server.listen(1)
            self.server.settimeout(1)
            print("Waiting for clients...")
            threading.Thread(target=self.accept).start()
        except Exception as e:
            print(e)
        while True:
            try:
                for x in self.clientsockets:
                    x[0].send(bytes("GETPOS=", "utf-8"))
                    temp = x[0].recv(1024).decode("utf-8")
                    temp = temp.replace("POS=", "")
                    temp = temp.split(",")
                    for y in temp:
                        y = int(y)
                    print(
                        f"{x[0].getpeername()} send:\nx: {temp[0]} y: {temp[1]}")
                    self.clientPositions[self.clientsockets.index(x)] = temp
                    sleep(1)
            except Exception as e:
                print(e)

    def joinGame(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((socket.gethostname(), 1234))
        print("Connected to server!")
        while True:
            data = self.clientsocket.recv(1024).decode("utf-8")
            if data == "GETPOS=":
                # self.clientsocket.send(bytes(f"POS={200},{700}", "utf-8"))
                self.clientsocket.send(bytes(
                    f"POS={self.window.player.center_x},{self.window.player.center_y}", "utf-8"))


if __name__ == '__main__':
    # check if the user wants to host or join a game
    if sys.argv[1] == "host":
        server = Server(True)
        print("starting server as host")
    elif sys.argv[1] == "join":
        server = Server(False)
        print("starting server as client")
    else:
        print("Invalid argument!")
        exit()
    serverThread = threading.Thread(target=server.start)
    serverThread.start()
    while True:
        # look if the project X game is still running, if not exit the server
        if server.host:
            # update the player positions
            for x in server.clientsockets:
                print(x[0].getpeername())