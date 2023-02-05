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
        threading.Thread(target=self.getAllPositions).start()

    def getAllPositions(self):
        while True:
            try:
                # get all the positions from the clients
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

                # get all the positions and send them to the clients
                if len(self.clientsockets) > 0:
                    with open("code\\playerPositions.json", "r") as f:
                        temp = "POS="
                        data = json.load(f)
                        for x in data["players"]:
                            temp += f"{x['id']},{x['x']},{x['y']};"
                        for x in self.clientsockets:
                            x[0].send(bytes(temp, "utf-8"))
            except Exception as e:
                print(e)

    def joinGame(self):
        # connect to the server
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((socket.gethostname(), 1234))
        print("Connected to server!")
        while True:
            data = self.clientsocket.recv(1024).decode("utf-8")
            print(data)
            # get all the player positions from the server
            if data == "POS=":
                self.clientsocket.send(bytes("GETPOS=", "utf-8"))
                temp = self.clientsocket.recv(1024).decode("utf-8")
                temp = temp.replace("POS=", "")
                temp = temp.split(";")
                for x in temp:
                    playerData = x.split(",")
                    print(
                        f"Player {playerData[0]} is at x: {playerData[1]} y: {playerData[2]}")
                    with open("code\\playerPositions.json", "r+") as f:
                        data = json.load(f)
                        # update the player positions
                        data["players"][playerData[0]]["x"] = playerData[1]
                        data["players"][playerData[0]]["y"] = playerData[2]
                        print(data)
                        f.seek(0)
                        json.dump(data, f)
                        f.truncate()

            # send our player position to the server
            elif data == "GETPOS=":
                with open("code\\playerPositions.json", "r") as f:
                    data = json.load(f)
                    x = data["players"]["0"]["x"]
                    y = data["players"]["0"]["y"]
                self.clientsocket.send(bytes(
                    f"POS={x},{y}", "utf-8"))


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
