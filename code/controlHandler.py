import arcade
from entities import Player


class MenuController:

    def __init__(self, gamewindow: arcade.Window, controls: list):
        self.controlDict = {
            "up": arcade.key.W,
            "down": arcade.key.S,
            "left": arcade.key.A,
            "right": arcade.key.D,
            "select": arcade.key.ENTER,
            "back": arcade.key.ESCAPE,
        }
        # controls is a list of tuples, each tuple is a key and a short string of what to do
        self.controls = controls
        self.gamewindow = gamewindow
        for x in controls:
            if x[1] in self.controlDict.keys():
                self.controlDict[x[1]] = x[0]

    def handle_input(self, key):
        if self.gamewindow.mapSelectActive:
            if key == self.controlDict["up"]:
                self.gamewindow.menuItemSelected -= 4
                if self.gamewindow.menuItemSelected < 0:
                    self.gamewindow.menuItemSelected = 0
            elif key == self.controlDict["down"]:
                self.gamewindow.menuItemSelected += 4
                if self.gamewindow.menuItemSelected > len(self.gamewindow.mapSelectItems)-1:
                    self.gamewindow.menuItemSelected = len(
                        self.gamewindow.mapSelectItems)-1
            elif key == self.controlDict["left"]:
                if self.gamewindow.menuItemSelected > 0:
                    self.gamewindow.menuItemSelected -= 1
            elif key == self.controlDict["right"]:
                if self.gamewindow.menuItemSelected < len(self.gamewindow.mapSelectItems)-1:
                    self.gamewindow.menuItemSelected += 1

        else:
            if key == self.controlDict["up"]:
                if self.gamewindow.menuItemSelected > 0:
                    self.gamewindow.menuItemSelected -= 1
            elif key == self.controlDict["down"]:
                if self.gamewindow.menuItemSelected < len(self.gamewindow.menuItems)-1:
                    self.gamewindow.menuItemSelected += 1


class PlayerController:
    def __init__(self, gamewindow: arcade.Window, player: Player,  controls: list):
        self.controlDict = {
            "up": arcade.key.W,
            "down": arcade.key.S,
            "left": arcade.key.A,
            "right": arcade.key.D,
            "shoot": arcade.key.SPACE,
        }
        self.controls = controls
        self.gamewindow = gamewindow
        self.player = player
        print("init controls")
        print(controls)
        for x in controls:
            if x[1] in self.controlDict.keys():
                print("setting keys to: ", x[0], " for ", x[1])
                self.controlDict[x[1]] = x[0]

    def handle_input(self, key):
        if key == self.controlDict["up"]:
            if self.player.in_air:
                self.player.change_y += 12
            else:
                self.player.change_y = 10
        elif key == self.controlDict["down"]:
            if self.player.in_air:
                self.player.change_y -= 12
            else:
                self.player.change_y = -10
        elif key == self.controlDict["left"]:
            self.player.facing = "left"
            if self.player.in_air:
                self.player.change_x -= 12
            else:
                self.player.change_x = -10
        elif key == self.controlDict["right"]:
            self.player.facing = "right"
            if self.player.in_air:
                self.player.change_x += 12
            else:
                self.player.change_x = 10
        elif key == self.controlDict["shoot"]:
            self.player.updatePowerup()
            if self.player.powerup == "line":
                self.player.shoot(200, 15, 7, 0, 0, "line")
            elif self.player.powerup == "shotgun":
                for i in range(-20, 21, 20):
                    self.player.shoot(5, 15, 20, i/10, i, "shotgun")
            else:
                self.player.shoot(5, 15, 20)
