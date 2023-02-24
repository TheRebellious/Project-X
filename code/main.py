import json
import os
import threading
import arcade
from entities import Player

WINDOW_X = 1920
WINDOW_Y = 1080
TITLE = "Project X"


class GameWindow(arcade.Window):
    menuActive = True
    menuItemSelected = 0
    titlescreenItems = ["Host Game", "Join Game",
                        "Split screen", "Controls", "Exit"]
    menuItems = titlescreenItems
    server = None

    optionsMenuActive = False
    optionsMenuItems = ["Back"]

    gameActive = False
    splitScreen = False
    colorDict = {
        "grey": arcade.color.ASH_GREY,
        "aspargus": arcade.color.GRAY_ASPARAGUS,
        "green": arcade.color.GREEN,
        "blue": arcade.color.LIGHT_BLUE,
        "red": arcade.color.RED,
        "yellow": arcade.color.YELLOW,
        "black": arcade.color.BLACK,
        "white": arcade.color.WHITE,
        "brown": arcade.color.BROWN,
        "orange": arcade.color.ORANGE,
        "purple": arcade.color.PURPLE,
        "pink": arcade.color.PINK,
        "cyan": arcade.color.CYAN,
    }

    damage = {
        "line": 50,
        "shotgun": 10,
        "none": 10,
    }

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.AMAZON)
        self.set_fullscreen(True)
        self.level = None
        self.levels = {
            "Stalingrad": "stalingrad.json",
        }
        self.entities = []
        self.player2 = None
        self.player = None

    def on_draw(self):
        if self.splitScreen:
            if self.player is not None and self.gameActive:
                self.player.update()
            if self.player2 is not None and self.gameActive:
                self.player2.update()
            for x in self.entities:
                x.update()

        else:
            if self.player is not None and self.gameActive:
                self.player.update()
                for x in self.entities:
                    x.update()

        arcade.start_render()

        if self.menuActive:
            self.draw_menu()
        if self.optionsMenuActive:
            self.draw_options_menu()
        if self.gameActive:
            self.draw_game()
            self.collisions(
                self.player, self.level["objects"])
            self.getEntityCollisions(self.player, self.entities)
            if self.splitScreen:
                self.collisions(
                    self.player2, self.level["objects"])
                self.getEntityCollisions(self.player2, self.entities)
        arcade.finish_render()

    # Draws a menu screen using arcade functions and is able to move around with the wasd keys
    # if the menuItem is selected, it will be highlighted
    def draw_menu(self):
        # draw title text
        arcade.draw_text("Project X", WINDOW_X / 2, WINDOW_Y /
                         2 + 200, arcade.color.WHITE, 100, anchor_x="center")
        # draw menu items
        for i in range(len(self.menuItems)):
            if i == self.menuItemSelected:
                arcade.draw_text(self.menuItems[i], WINDOW_X / 2, WINDOW_Y /
                                 2 - 70 * i, arcade.color.WHITE, 50, anchor_x="center")
            else:
                arcade.draw_text(self.menuItems[i], WINDOW_X / 2, WINDOW_Y /
                                 2 - 70 * i, arcade.color.BLACK, 50, anchor_x="center")

    def draw_options_menu(self):
        for i in range(len(self.optionsMenuItems)):
            arcade.draw_text("WASD to move around", WINDOW_X / 2, WINDOW_Y /
                             2 + 200, arcade.color.BLACK, 50, anchor_x="center")
            arcade.draw_text("WS and UP and DOWN to move through menu", WINDOW_X / 2,
                             WINDOW_Y / 2 + 100, arcade.color.BLACK, 50, anchor_x="center")
            arcade.draw_text("ENTER to select menu item", WINDOW_X / 2,
                             WINDOW_Y / 2, arcade.color.BLACK, 50, anchor_x="center")
            if i == self.menuItemSelected:
                arcade.draw_text(self.optionsMenuItems[i], WINDOW_X / 2, WINDOW_Y / 2 - (
                    100 * i)-100, arcade.color.WHITE, 50, anchor_x="center")
            else:
                arcade.draw_text(self.optionsMenuItems[i], WINDOW_X / 2, WINDOW_Y / 2 - (
                    100 * i)-100, arcade.color.BLACK, 50, anchor_x="center")

    # uses a series of functions to draw the game
    def draw_game(self):
        self.draw_level()
        self.draw_entities()
        if not self.splitScreen:
            with open("code\\playerPositions.json", "r+") as playerPositions:
                playerPositions = json.load(playerPositions)
            for i in playerPositions["players"]:
                if self.player is None:
                    # find the first available player and make it the player
                    for x in playerPositions["players"]:
                        if x["visible"] == False:
                            self.player = Player(
                                self, x["id"], 1, 0.25, 0.5, x["name"])
                            # set the player's position to the position of the player in the json file
                            playerPositions["players"][x["id"]
                                                       ]["x"] = self.player.center_x
                            playerPositions["players"][x["id"]
                                                       ]["y"] = self.player.center_y
                            # set the player's visibility to true
                            playerPositions["players"][x["id"]
                                                       ]["visible"] = True
                            # write the changes to the json file
                            with open("code\\playerPositions.json", "w") as f:
                                json.dump(playerPositions, f, indent=4)
                            break
                if i["visible"]:
                    if i["id"] == self.player.id:
                        pass
                    x = i["x"]
                    y = i["y"]
                    color = i["name"]
                    player = Player(self, i["id"], 1, 0.25, 0.5, color)
                    player.center_x = x
                    player.center_y = y
                    self.draw_player(player)
            self.draw_player(self.player)
        else:
            if self.player is not None:
                self.draw_player(self.player)
            else:
                self.player = Player(self, 0, 1, 0.25, 0.5, "red")
            if self.player2 is not None:
                self.draw_player(self.player2)
            else:
                self.player2 = Player(self, 1, 1, 0.25, 0.5, "yellow")

    # draws a level defined in the levels dictionary which references a json file

    def draw_level(self):
        with open("assets\\levels\\" + self.levels["Stalingrad"]) as level:
            self.level = json.load(level)
        for i in self.level["objects"]:
            x = i["x"]
            y = i["y"]
            width = i["width"]
            height = i["height"]
            arcade.draw_rectangle_filled(
                x+(width/2), y+(height/2), width, height, self.colorDict[i["color"]])

    def draw_player(self, player: Player):
        width = player.width
        height = player.height
        x = player.center_x
        y = player.center_y
        color = player.color
        # placeholder for the player is a box
        arcade.draw_rectangle_filled(
            x, y+(height/2), width, height, color)

    def draw_entities(self):
        for i in self.entities:
            x = i.center_x
            y = i.center_y
            width = i.width
            height = i.height
            color = i.color
            arcade.draw_rectangle_filled(x, y, width, height, color)

    def getEntityCollisions(self, player: Player, entities: list):
        for i in entities:
            # print the difference between the y values of the player and the entity
            print(i.center_y - (i.height/2) - player.center_y, i.center_y + (i.height/2) - (player.center_y+50),
                  i.center_x - (i.width/2) - player.center_x, i.center_x + (i.width/2) - player.center_x+(player.width/2))
            if i.center_x - (i.width/2) > player.center_x - (player.width / 2) and i.center_x + (i.width/2) < player.center_x + (player.width / 2) and i.center_y - (i.height/2) < player.center_y and i.center_y + i.height > player.center_y + (player.height / 2):
                # print("hit")
                player.hp -= self.damage[player.powerup]
                self.entities.remove(i)

    def collisions(self, player, objects: list):
        # return the x and y speeds to make the player not collide with the objects it is colliding with
        for i in objects:
            if i["collision"] == True:
                if player.center_y - (player.height/2) > i["y"] and player.center_y - (player.height/2) < i["y"] + i["height"] and player.center_x + (player.width / 2) > i["x"] and player.center_x - (player.width / 2) < i["x"] + i["width"]:
                    if player.change_y < 0:
                        if player.change_y < -7:
                            player.change_y = 5
                        else:
                            player.change_y = 0
                        player.center_y = i["y"] + i["height"]
                        player.in_air = False
                        player.on_ground = True
            else:
                player.in_air = True
                player.on_ground = False

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER and self.menuActive:
            if self.menuItems[self.menuItemSelected] == "Host Game":
                self.host = True
                self.menuItemSelected = 0
                self.menuActive = False
                self.gameActive = True
                threading.Thread(target=os.system, args=(
                    "python code/connection.py host",)).start()
            if self.menuItems[self.menuItemSelected] == "Join Game":
                self.host = False
                self.menuItemSelected = 0
                self.menuActive = False
                self.gameActive = True
                threading.Thread(target=os.system, args=(
                    "python code/connection.py join",)).start()
            if self.menuItems[self.menuItemSelected] == "Split screen":
                self.splitScreen = True
                self.menuItemSelected = 0
                self.menuActive = False
                self.gameActive = True

            if self.menuItems[self.menuItemSelected] == "Controls":
                self.menuItemSelected = 0
                self.menuActive = False
                self.optionsMenuActive = True
                self.menuItems = self.optionsMenuItems
            if self.menuItems[self.menuItemSelected] == "Exit":
                arcade.close_window()
        elif key == arcade.key.ENTER and self.optionsMenuActive:
            if self.optionsMenuItems[self.menuItemSelected] == "Back":
                self.menuItemSelected = 0
                self.menuActive = True
                self.optionsMenuActive = False
                self.menuItems = self.titlescreenItems
        # change the menu item selected
        elif self.menuActive or self.optionsMenuActive:
            if (key == arcade.key.W or key == arcade.key.UP) and self.menuItemSelected > 0:
                self.menuItemSelected -= 1
            if (key == arcade.key.S or key == arcade.key.DOWN) and self.menuItemSelected < len(self.menuItems) - 1:
                self.menuItemSelected += 1
        if self.gameActive and self.splitScreen:
            if key == arcade.key.T:
                self.player.powerupCounter = 3
                self.player2.powerupCounter = 3
                self.player.powerup = "line"
                self.player2.powerup = "line"

            # player 1 controls
            if self.player is not None:
                if key == arcade.key.W:
                    if self.player.in_air:
                        self.player.change_y += 12
                    else:
                        self.player.change_y = 10
                elif key == arcade.key.S:
                    if self.player.in_air:
                        self.player.change_y -= 12
                    else:
                        self.player.change_y = -10
                elif key == arcade.key.A:
                    self.player.facing = "left"
                    if self.player.in_air:
                        self.player.change_x -= 12
                    else:
                        self.player.change_x = -10
                elif key == arcade.key.D:
                    self.player.facing = "right"
                    if self.player.in_air:
                        self.player.change_x += 12
                    else:
                        self.player.change_x = 10
                elif key == arcade.key.SPACE:
                    self.player.updatePowerup()
                    if self.player.powerup == "line":
                        self.player.shoot(200, 15, 7)
                    elif self.player.powerup == "shotgun":
                        for i in range(-20, 20, 14):
                            self.player.shoot(5, 15, 20, i)
                    else:
                        self.player.shoot(5, 15, 20)

            # player 2 controls
            if self.player2 is not None:
                if key == arcade.key.UP:
                    if self.player2.in_air:
                        self.player2.change_y += 12
                    else:
                        self.player2.change_y = 10
                elif key == arcade.key.DOWN:
                    if self.player2.in_air:
                        self.player2.change_y -= 12
                    else:
                        self.player2.change_y = -10
                elif key == arcade.key.LEFT:
                    self.player2.facing = "left"
                    if self.player2.in_air:
                        self.player2.change_x -= 12
                    else:
                        self.player2.change_x = -10
                elif key == arcade.key.RIGHT:
                    self.player2.facing = "right"
                    if self.player2.in_air:
                        self.player2.change_x += 12
                    else:
                        self.player2.change_x = 10
                elif key == arcade.key.ENTER:
                    self.player2.updatePowerup()
                    if self.player2.powerup == "line":
                        self.player2.shoot(200, 15, 7)
                    else:
                        self.player2.shoot(5, 15, 20)

        # multiplayer controls
        else:
            if key == arcade.key.W:
                if self.player.in_air:
                    self.player.change_y += 12
                else:
                    self.player.change_y = 10
            if key == arcade.key.S:
                if self.player.in_air:
                    self.player.change_y -= 12
                else:
                    self.player.change_y = -10
            if key == arcade.key.A:
                self.player.facing = "left"
                if self.player.in_air:
                    self.player.change_x -= 12
                else:
                    self.player.change_x = -10
            if key == arcade.key.D:
                self.player.facing = "right"
                if self.player.in_air:
                    self.player.change_x += 12
                else:
                    self.player.change_x = 10
            if key == arcade.key.SPACE:
                self.player.shoot()


if __name__ == "__main__":
    with open("playerPositions.json", "r") as f:
        playerPositions = json.load(f)
    with open("code\\playerPositions.json", "w") as f:
        json.dump(playerPositions, f, indent=4)
    window = GameWindow(WINDOW_X, WINDOW_X, TITLE)
    arcade.run()
    # shtudown the server
    os.system("taskkill /f /im python.exe")
