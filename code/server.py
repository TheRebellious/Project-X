import asyncio
import socket
import threading
from time import sleep
import arcade


class Server:
    clientsockets = []
    clientPositions = []

    def __init__(self, Host: bool, window: arcade.Window) -> None:
        self.host = Host
        self.window = window

    async def start(self):
        if self.host:
            hostTask = asyncio.create_task(self.hostGame()) 
        else:
            clientTask = asyncio.create_task(self.joinGame()) 
        while True:
            await asyncio.sleep(1)

    async def accept(self):
        while True:
            try:
                # print("Waiting for connection...")
                self.clientsockets.insert(0, self.server.accept())
                self.clientPositions.insert(0, [0, 0])
                print(
                    f"Connection from {self.clientsockets[0][0]} has been established!")
            except:
                pass
                # print("Connection timed out!")

    async def hostGame(self):
        try:
            print("Starting server...")
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(("", 1234))
            print("Server started!")
            self.server.listen(1)
            self.server.settimeout(1)
            print("Waiting for clients...")
            asyncio.create_task(self.accept())
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
                    print(f"{x[0].getpeername()} send:\nx: {temp[0]} y: {temp[1]}")
                    self.clientPositions[self.clientsockets.index(x)] = temp
                    sleep(1)
            except Exception as e:
                print(e)

    async def joinGame(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((socket.gethostname(), 1234))
        print("Connected to server!")
        while True:
            data = self.clientsocket.recv(1024).decode("utf-8")
            if data == "GETPOS=":
                # self.clientsocket.send(bytes(f"POS={200},{700}", "utf-8"))
                self.clientsocket.send(bytes(f"POS={self.window.player.center_x},{self.window.player.center_y}", "utf-8"))


# server = Server(True, None)
# threading.Thread(target=server.start).start()
# sleep(0.5)
# client = Server(False, None)
# threading.Thread(target=client.start).start()