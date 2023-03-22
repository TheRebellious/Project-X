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

    def draw_map_select(self):
        for x in self.gamewindow.mapSelectItems:
            textcolor = arcade.color.BLACK
            if self.gamewindow.mapSelectItems.index(x) == self.gamewindow.menuItemSelected:
                textcolor = arcade.color.WHITE
            if (self.gamewindow.mapSelectItems.index(x)) > 3:

                arcade.draw_text(x, (400 * (self.gamewindow.mapSelectItems.index(x)-3)
                                     )-32, 1080-850, textcolor, 50, anchor_x="center")
                self.draw_thumbnail(x, yAlignment=1080-800, xAlignment=(
                    400 * (self.gamewindow.mapSelectItems.index(x)-3)-232), scale=0.2)
            else:
                arcade.draw_text(x, (400 * (self.gamewindow.mapSelectItems.index(x)+1)
                                     )-32, 1080-450, textcolor, 42, anchor_x="center")
                self.draw_thumbnail(x, yAlignment=1080-400, xAlignment=(
                    400 * (self.gamewindow.mapSelectItems.index(x)+1)-232), scale=0.2)

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
        self.draw_powerups()
        self.draw_scores()
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
                self.gamewindow.player = Player(
                    self.gamewindow, 0, 1, 0.25, 0.25, "red")
                self.gamewindow.scores.append(0)
            if self.gamewindow.player2 is not None:
                self.draw_player(self.gamewindow.player2)
            else:
                self.gamewindow.player2 = Player(
                    self.gamewindow, 1, 1, 0.25, 0.25, "yellow")
                self.gamewindow.scores.append(0)

    def draw_thumbnail(self, levelstr, xAlignment=0, yAlignment=0, scale=0.2):
        with open("assets\\levels\\" + levelstr + ".json") as level:
            level = json.load(level)
        for i in level["objects"]:
            x = xAlignment + (i["x"]*scale)
            y = yAlignment + (i["y"]*scale)
            width = i["width"]*scale
            height = i["height"]*scale
            arcade.draw_rectangle_filled(
                x+(width/2), y+(height/2), width, height, self.gamewindow.colorDict[i["color"]])

    # draws a level defined in the levels dictionary which references a json file
    def draw_level(self):
        with open("assets\\levels\\" + self.gamewindow.selectedMap + ".json") as level:
            self.gamewindow.level = json.load(level)
        for i in self.gamewindow.level["objects"]:
            x = i["x"]
            y = i["y"]
            width = i["width"]
            height = i["height"]
            arcade.draw_rectangle_filled(
                x+(width/2), y+(height/2), width, height, self.gamewindow.colorDict[i["color"]])

    def draw_scores(self):
        for i in range(len(self.gamewindow.scores)):
            arcade.draw_text(self.gamewindow.scores[len(self.gamewindow.scores)-1-i], (self.WINDOW_X /
                             2 - 70 * i)+45, self.WINDOW_Y - 100, arcade.color.BLACK, 24, anchor_x="center")

    def draw_player(self, player: Player):
        width = player.width
        height = player.height
        x = player.center_x
        y = player.center_y
        color = player.color
        # placeholder for the player is a box
        arcade.draw_rectangle_filled(
            x, y+(height/2), width, height, color)
        arcade.draw_rectangle_outline(
            x, y+(height/2), width, height, arcade.color.BLACK, 2)
        self.draw_hp_bar(player)

    def draw_hp_bar(self, player: Player):
        x = player.center_x
        y = player.center_y
        color = player.color
        # draw the outline of the hp bar
        arcade.draw_rectangle_outline(x, y-10, 60, 10, arcade.color.BLACK, 2)
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
            arcade.draw_rectangle_outline(
                x, y, width, height, arcade.color.BLACK, 2)

    def draw_powerups(self):
        for i in self.gamewindow.powerups:
            if i is None:
                self.gamewindow.powerups.remove(i)
                continue
            x = i[0].center_x
            y = i[0].center_y
            width = i[0].width
            height = i[0].height
            powerup = i[0].powerup
            arcade.draw_rectangle_filled(
                x, y, width, height, arcade.color.WHITE)
            arcade.draw_rectangle_outline(
                x, y, width, height, arcade.color.BLACK, 2)
            if powerup == "shotgun":
                arcade.draw_text("3", x, y-10, arcade.color.RED,
                                 20, anchor_x="center")
            elif powerup == "line":
                arcade.draw_text("|", x, y-10, arcade.color.RED,
                                 20, anchor_x="center")
