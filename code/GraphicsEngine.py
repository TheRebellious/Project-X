import json
import arcade
from entities import Player


class GraphicsEngine():
    def __init__(self, gamewindow, x, y):
        print("GraphicsEngine init")
        print("MAX WIDTH: " + str(x))
        print("MAX HIGHT: " + str(y))
        super().__init__()
        self.gamewindow = gamewindow
        self.WINDOW_X = x
        self.WINDOW_Y = y

    def draw_menu(self):
        # draw title text
        arcade.draw_text("Project X", self.WINDOW_X / 2, self.WINDOW_Y /
                         2 + 200, arcade.color.WHITE, 100, anchor_x="center")
        # draw menu items
        for i in range(len(self.gamewindow.menuItems)):
            if i == self.gamewindow.menuItemSelected:
                arcade.draw_text(self.gamewindow.menuItems[i], self.WINDOW_X / 2, self.WINDOW_Y /
                                 2 - 70 * i, arcade.color.WHITE, 50, anchor_x="center")
            else:
                arcade.draw_text(self.gamewindow.menuItems[i], self.WINDOW_X / 2, self.WINDOW_Y /
                                 2 - 70 * i, arcade.color.BLACK, 50, anchor_x="center")

    def draw_options_menu(self):
        for i in range(len(self.gamewindow.optionsMenuItems)):
            arcade.draw_text("WASD to move around", self.WINDOW_X / 2, self.WINDOW_Y /
                             2 + 200, arcade.color.BLACK, 50, anchor_x="center")
            arcade.draw_text("WS and UP and DOWN to move through menu", self.WINDOW_X / 2,
                             self.WINDOW_Y / 2 + 100, arcade.color.BLACK, 50, anchor_x="center")
            arcade.draw_text("ENTER to select menu item", self.WINDOW_X / 2,
                             self.WINDOW_Y / 2, arcade.color.BLACK, 50, anchor_x="center")
            if i == self.gamewindow.menuItemSelected:
                arcade.draw_text(self.gamewindow.optionsMenuItems[i], self.WINDOW_X / 2, self.WINDOW_Y / 2 - (
                    100 * i)-100, arcade.color.WHITE, 50, anchor_x="center")
            else:
                arcade.draw_text(self.gamewindow.optionsMenuItems[i], self.WINDOW_X / 2, self.WINDOW_Y / 2 - (
                    100 * i)-100, arcade.color.BLACK, 50, anchor_x="center")

    # uses a series of functions to draw the game
    def draw_game(self):
        self.draw_level()
        self.draw_entities()
        if not self.gamewindow.splitScreen:
            with open("code\\playerPositions.json", "r+") as playerPositions:
                playerPositions = json.load(playerPositions)
            for i in playerPositions["players"]:
                if self.gamewindow.player is None:
                    # find the first available player and make it the player
                    for x in playerPositions["players"]:
                        if x["visible"] == False:
                            self.gamewindow.player = Player(
                                self.gamewindow, x["id"], 1, 0.25, 0.5, x["name"])
                            # set the player's position to the position of the player in the json file
                            playerPositions["players"][x["id"]
                                                       ]["x"] = self.gamewindow.player.center_x
                            playerPositions["players"][x["id"]
                                                       ]["y"] = self.gamewindow.player.center_y
                            # set the player's visibility to true
                            playerPositions["players"][x["id"]
                                                       ]["visible"] = True
                            # write the changes to the json file
                            with open("code\\playerPositions.json", "w") as f:
                                json.dump(playerPositions, f, indent=4)
                            break
                if i["visible"]:
                    if i["id"] == self.gamewindow.player.id:
                        pass
                    x = i["x"]
                    y = i["y"]
                    color = i["name"]
                    player = Player(self, i["id"], 1, 0.25, 0.5, color)
                    player.center_x = x
                    player.center_y = y
                    self.draw_player(player)
            self.draw_player(self.gamewindow.player)
        else:
            if self.gamewindow.player is not None:
                self.draw_player(self.gamewindow.player)
            else:
                self.gamewindow.player = Player(self.gamewindow, 0, 1, 0.25, 0.5, "red")
            if self.gamewindow.player2 is not None:
                self.draw_player(self.gamewindow.player2)
            else:
                self.gamewindow.player2 = Player(
                    self.gamewindow, 1, 1, 0.25, 0.5, "yellow")

    # draws a level defined in the levels dictionary which references a json file

    def draw_level(self):
        with open("assets\\levels\\" + self.gamewindow.levels["Stalingrad"]) as level:
            self.gamewindow.level = json.load(level)
        for i in self.gamewindow.level["objects"]:
            x = i["x"]
            y = i["y"]
            width = i["width"]
            height = i["height"]
            arcade.draw_rectangle_filled(
                x+(width/2), y+(height/2), width, height, self.gamewindow.colorDict[i["color"]])

    def draw_player(self, player: Player):
        width = player.width
        height = player.height
        x = player.center_x
        y = player.center_y
        color = player.color
        # placeholder for the player is a box
        arcade.draw_rectangle_filled(
            x, y+(height/2), width, height, color)
        self.draw_hp_bar(player)

    def draw_hp_bar(self, player: Player):
        x = player.center_x
        y = player.center_y
        color = player.color
        # draw the outline of the hp bar
        arcade.draw_rectangle_outline(x, y-10, 60, 10, arcade.color.BLACK)
        # fill in the hp bar
        arcade.draw_rectangle_filled(x, y-10, 60*(player.hp/100), 10, color)

    def draw_entities(self):
        for i in self.gamewindow.entities:
            x = i.center_x
            y = i.center_y
            width = i.width
            height = i.height
            color = i.color
            arcade.draw_rectangle_filled(x, y, width, height, color)
